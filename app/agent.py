# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import re
import json
import os
import sys
from zoneinfo import ZoneInfo

from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.adk.models import Gemini
from google.adk.tools import AgentTool
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.workflow import Workflow, node, START
from google.genai import types
from pydantic import BaseModel, Field

from app.config import config

# Define output schema for orchestrator to ensure structured data routing
class CareerCoachOutput(BaseModel):
    response: str = Field(description="The detailed career advice response.")
    recommended_next_steps: list[str] = Field(description="A list of 2-3 recommended next steps.")

# Initialize the Gemini model with configured model and retries
model_inst = Gemini(
    model=config.model,
    retry_options=types.HttpRetryOptions(attempts=3),
)

# ── Local MCP Server Configuration ──
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mcp_script = os.path.join(PROJECT_ROOT, "app", "mcp_server.py")

mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[mcp_script],
        ),
    ),
)

# ── Specialized Sub-Agents ──

resume_agent = LlmAgent(
    name="resume_agent",
    model=model_inst,
    instruction="""You are a professional resume reviewer. 
Review the user's resume content, suggest formatting enhancements, identify grammatical issues, 
and recommend stronger action verbs. Be encouraging but highly critical of resume best practices.""",
    description="Analyzes resumes, suggests formatting, wording, and action verb improvements."
)

interview_agent = LlmAgent(
    name="interview_agent",
    model=model_inst,
    instruction="""You are an expert technical and behavioral interviewer.
Conduct mock interviews, provide job-specific questions, evaluate user answers, and supply model answers to prepare the user for success.
Use the search_interview_questions tool to find relevant question guidelines for the user's target job title.""",
    tools=[mcp_toolset],
    description="Provides mock interview questions, preparation tips, and model answers."
)

planner_agent = LlmAgent(
    name="planner_agent",
    model=model_inst,
    instruction="""You are a strategic career planner. 
Generate detailed learning paths, recommended projects, career roadmaps, and transition plans based on target roles and current skills.
Use the get_career_resources tool to find learning materials and get_project_ideas to suggest portfolio projects.""",
    tools=[mcp_toolset],
    description="Creates learning roadmaps, career plans, and project suggestions."
)

# ── Orchestrator Agent ──

orchestrator = LlmAgent(
    name="orchestrator",
    model=model_inst,
    instruction="""You are CareerForge AI, a career development coach.
Coordinate with the specialized agents (resume_agent, interview_agent, planner_agent) to assist the user.
The user's query: {cleaned_prompt}
User feedback on previous plan (if any): {user_feedback}

Determine which specialized sub-agent is appropriate.
If the query is about resume review, delegate to resume_agent.
If it is about mock interviews or interview preparation, delegate to interview_agent.
If it is about learning plans, career paths, or project suggestions, delegate to planner_agent.
If it involves multiple parts, consult them sequentially.
Synthesize their outputs into a structured CareerCoachOutput response.
""",
    tools=[AgentTool(resume_agent), AgentTool(interview_agent), AgentTool(planner_agent)],
    output_schema=CareerCoachOutput,
    output_key="orchestrator_output"
)

# ── Workflow Function Nodes ──

def security_checkpoint(ctx: Context, node_input: types.Content) -> Event:
    """Checks input for prompt injections, scrubs PII, and applies domain-specific rules."""
    text = ""
    if hasattr(node_input, 'parts') and node_input.parts:
        text = "".join([p.text for p in node_input.parts if p.text])
    elif isinstance(node_input, str):
        text = node_input
    
    # Initialize state variables
    ctx.state["cleaned_prompt"] = text
    ctx.state["user_feedback"] = ""
    
    # PII Scrubbing (Email address redaction)
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    if re.search(email_pattern, text):
        text = re.sub(email_pattern, "[REDACTED EMAIL]", text)
        ctx.state["cleaned_prompt"] = text
        audit_log = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "severity": "WARNING",
            "event": "PII_REDACTION",
            "details": "Email detected and redacted."
        }
        print(f"AUDIT LOG: {json.dumps(audit_log)}")

    # Prompt Injection Detection
    injection_keywords = ["ignore previous instructions", "system prompt", "you must bypass", "override rules"]
    detected = False
    for keyword in injection_keywords:
        if keyword in text.lower():
            detected = True
            break
            
    if detected:
        audit_log = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "severity": "CRITICAL",
            "event": "PROMPT_INJECTION",
            "details": "Potential prompt injection keywords found."
        }
        print(f"AUDIT LOG: {json.dumps(audit_log)}")
        return Event(output="Security Blocked: Potential policy violation detected in input.", route="blocked")

    # Domain-Specific Rule: career alignment check (non-blocking, logged)
    career_keywords = ["resume", "job", "career", "interview", "learn", "skill", "project", "hire", "recruiter", "work", "cv", "portfolio"]
    is_career = any(kw in text.lower() for kw in career_keywords)
    if not is_career and len(text) > 0:
        audit_log = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "severity": "INFO",
            "event": "ALIGNMENT_WARNING",
            "details": "Query does not appear career-related."
        }
        print(f"AUDIT LOG: {json.dumps(audit_log)}")
        
    audit_log = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "severity": "INFO",
        "event": "SECURITY_PASSED",
        "details": "Input passed security checks."
    }
    print(f"AUDIT LOG: {json.dumps(audit_log)}")
    return Event(output=text, route="passed")


def security_block(node_input: str) -> Event:
    """Terminal node when request fails security checks."""
    content = types.Content(
        role="model",
        parts=[types.Part.from_text(text=node_input)]
    )
    yield Event(content=content)
    yield Event(output={"error": node_input})


@node(rerun_on_resume=True)
async def human_approval_node(ctx: Context, node_input: dict) -> Event:
    """Pauses for human confirmation or feedback on the suggested career guidance."""
    response_text = node_input.get("response", "")
    next_steps = node_input.get("recommended_next_steps", [])
    
    formatted_content = (
        f"### Career Coach Plan Suggestions\n\n{response_text}\n\n"
        f"**Next Steps:**\n" + "\n".join([f"- {step}" for step in next_steps])
    )
    
    # Emit UI content for the user to view in playground
    yield Event(content=types.Content(role="model", parts=[types.Part.from_text(text=formatted_content)]))
    
    # Check for HITL response in resume inputs
    if not ctx.resume_inputs or "approval" not in ctx.resume_inputs:
        yield RequestInput(
            interrupt_id="approval",
            message="Do you approve this career plan? (Type 'approve' or describe changes you want)."
        )
        return
        
    user_decision = ctx.resume_inputs["approval"]
    if "approve" in user_decision.lower():
        yield Event(output=node_input, route="approved")
    else:
        ctx.state["user_feedback"] = user_decision
        yield Event(output=user_decision, route="needs_revision")


def finalize_output_node(node_input: dict) -> Event:
    """Formats and displays the finalized approved output."""
    response_text = node_input.get("response", "")
    next_steps = node_input.get("recommended_next_steps", [])
    
    final_text = (
        f"✅ **Plan Approved!**\n\nHere is your finalized career plan:\n\n{response_text}\n\n"
        f"**Recommended Next Steps:**\n" + "\n".join([f"- {step}" for step in next_steps])
    )
    
    yield Event(content=types.Content(role="model", parts=[types.Part.from_text(text=final_text)]))
    yield Event(output=node_input)


# ── Workflow Graph Definition ──

root_agent = Workflow(
    name="careerforge_workflow",
    edges=[
        ('START', security_checkpoint),
        (security_checkpoint, {'blocked': security_block, 'passed': orchestrator}),
        (orchestrator, human_approval_node),
        (human_approval_node, {'needs_revision': orchestrator, 'approved': finalize_output_node})
    ],
    description="Multi-agent career development coach utilizing specialized sub-agents and Human-in-the-Loop approval."
)


app = App(
    root_agent=root_agent,
    name="app",
)
