import sys
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("CareerForge-MCP-Server")

@mcp.tool()
def get_career_resources(domain: str) -> str:
    """Returns curated learning resources, online courses, and certifications for a given career domain.

    Args:
        domain: The career domain name (e.g., 'software engineering', 'product management', 'data science', 'digital marketing').
    """
    domain_lower = domain.lower()
    
    resources = {
        "software engineering": (
            "### Curated Software Engineering Resources:\n"
            "- **Courses**: *CS50: Introduction to Computer Science* (edX), *Python for Everybody* (Coursera).\n"
            "- **Books**: *Clean Code* by Robert C. Martin, *Designing Data-Intensive Applications* by Martin Kleppmann.\n"
            "- **Certifications**: AWS Certified Solutions Architect, Google Cloud Associate Cloud Engineer.\n"
            "- **Platforms**: LeetCode, GitHub, Exercism."
        ),
        "product management": (
            "### Curated Product Management Resources:\n"
            "- **Courses**: *Brand and Product Management* (Coursera), *Product Management First Steps* (LinkedIn Learning).\n"
            "- **Books**: *Inspired: How to Create Tech Products Customers Love* by Marty Cagan, *The Design of Everyday Things* by Don Norman.\n"
            "- **Certifications**: Pragmatic Institute Product Certification, Certified Scrum Product Owner (CSPO).\n"
            "- **Platforms**: Product School, Mind the Product."
        ),
        "data science": (
            "### Curated Data Science Resources:\n"
            "- **Courses**: *Machine Learning Specialization* by Andrew Ng (Coursera), *Data Science MicroMasters* (edX).\n"
            "- **Books**: *Introduction to Statistical Learning* by Gareth James, *Python for Data Analysis* by Wes McKinney.\n"
            "- **Certifications**: Google Professional Data Engineer, Microsoft Certified: Azure Data Scientist Associate.\n"
            "- **Platforms**: Kaggle, DataCamp, Towards Data Science."
        )
    }
    
    # Fallback/default response if domain not exactly matched
    for key, val in resources.items():
        if key in domain_lower or domain_lower in key:
            return val
            
    return (
        f"### Curated Resources for '{domain}':\n"
        f"- **General Learning**: Look for foundational courses on Coursera, edX, or Udemy related to {domain}.\n"
        f"- **Reading**: Search for top-rated books on Amazon or Goodreads in the field of {domain}.\n"
        f"- **Certifications**: Check major cloud/industry providers (Google, AWS, Microsoft, PMI) for certifications in {domain}."
    )


@mcp.tool()
def get_project_ideas(role: str) -> str:
    """Returns 3 structured portfolio project ideas with descriptions, tech stacks, and key features for a target role.

    Args:
        role: The target professional role (e.g., 'frontend developer', 'backend developer', 'data analyst').
    """
    role_lower = role.lower()
    
    if "frontend" in role_lower:
        return (
            "### Recommended Frontend Portfolio Projects:\n\n"
            "1. **Personal Finance Dashboard**\n"
            "   - *Description*: A responsive SPA visualizing income, expenses, and savings goals.\n"
            "   - *Tech Stack*: React/Vue.js, Tailwind CSS, Chart.js, LocalStorage.\n"
            "   - *Key Features*: Interactive charts, transactions filtering, budget alerts.\n\n"
            "2. **Real-time Collaborative Kanban Board**\n"
            "   - *Description*: Trello clone with drag-and-drop support and real-time updates.\n"
            "   - *Tech Stack*: React, Firebase (Firestore), Tailwind CSS, React-beautiful-dnd.\n"
            "   - *Key Features*: Board customization, drag-and-drop lists/cards, user auth.\n\n"
            "3. **Recipe Finder & Meal Planner**\n"
            "   - *Description*: App that searches recipes by ingredients and schedules meals.\n"
            "   - *Tech Stack*: Vanilla JS or React, Spoonacular API, CSS Grid.\n"
            "   - *Key Features*: Search-by-ingredient filters, favorites lists, calendar planning."
        )
    elif "backend" in role_lower:
        return (
            "### Recommended Backend Portfolio Projects:\n\n"
            "1. **E-commerce RESTful API**\n"
            "   - *Description*: Scalable backend API supporting product catalog, cart, and payment flow.\n"
            "   - *Tech Stack*: Python (FastAPI/Django) or Node.js (Express), PostgreSQL, Redis, Stripe API.\n"
            "   - *Key Features*: JWT auth, database migrations, Stripe checkout integration, caching.\n\n"
            "2. **Task Queue & Email Notification Microservice**\n"
            "   - *Description*: Asynchronous job processing backend for triggering automated email/Slack alerts.\n"
            "   - *Tech Stack*: Go or Python, RabbitMQ/Celery, Redis, SendGrid API.\n"
            "   - *Key Features*: Worker pooling, rate limiting, message retries, detailed logging.\n\n"
            "3. **File Storage & Metadata Management System**\n"
            "   - *Description*: Secure API for uploading, resizing, and storing files with metadata extraction.\n"
            "   - *Tech Stack*: Node.js, AWS S3 / Google Cloud Storage, MongoDB.\n"
            "   - *Key Features*: Presigned URLs, image compression workers, tag search."
        )
    else:
        return (
            f"### Recommended Projects for '{role}':\n\n"
            f"1. **Interactive Portfolio Project**\n"
            f"   - *Description*: Showcase skills and case studies relevant to {role}.\n"
            f"   - *Key Features*: Sleek UI, detailed descriptions of problem/solution/impact.\n\n"
            f"2. **Automated Tool / Script**\n"
            f"   - *Description*: Build a utility script to automate a tedious task in the day-to-day workflow of a {role}.\n"
            f"   - *Key Features*: Command-line interface, configuration file, error handling.\n\n"
            f"3. **Industry Case Study / Report**\n"
            f"   - *Description*: Compile a deep-dive data analysis or audit report for a company operating in the {role} field.\n"
            f"   - *Key Features*: Structured writing, clear visuals, data-driven recommendations."
        )


@mcp.tool()
def search_interview_questions(job_title: str) -> str:
    """Searches and retrieves mock interview questions and ideal answer structures for a job title.

    Args:
        job_title: The job title to search questions for (e.g., 'software engineer', 'product manager').
    """
    title_lower = job_title.lower()
    
    if "software" in title_lower or "engineer" in title_lower or "developer" in title_lower:
        return (
            "### Mock Interview Prep: Software Engineer\n\n"
            "**Question 1 (Technical)**: Explain the difference between SQL and NoSQL databases. When would you choose which?\n"
            "- *Ideal Answer Structure*: Define relational vs non-relational. Discuss schema requirements (fixed vs dynamic), scaling properties (vertical vs horizontal), and transaction requirements (ACID vs BASE). Give examples (PostgreSQL vs MongoDB).\n\n"
            "**Question 2 (Behavioral)**: Describe a time you had to deal with technical debt or a system outage.\n"
            "- *Ideal Answer Structure (STAR)*: **Situation**: Explain the application and severity. **Task**: What was your responsibility. **Action**: How you diagnosed the issue and worked with the team to fix it. **Result**: System recovery, post-mortem, and long-term prevention plan."
        )
    elif "product" in title_lower or "manager" in title_lower:
        return (
            "### Mock Interview Prep: Product Manager\n\n"
            "**Question 1 (Product Design)**: How would you improve Google Maps for tourists?\n"
            "- *Ideal Answer Structure*: Identify goals (enhance tourist engagement/utility). Segment users (backpackers, families, business travelers). Brainstorm pain points (finding local hidden spots, language barriers). Propose features (curated audio guides, offline cultural tips). Prioritize using RICE framework.\n\n"
            "**Question 2 (Behavioral)**: Tell me about a time you had a conflict with engineering regarding a feature launch.\n"
            "- *Ideal Answer Structure (STAR)*: **Situation**: Feature scope conflict. **Task**: Align teams without delaying launch. **Action**: Run a collaborative trade-off session showing customer impact data. **Result**: Compromised on V1 MVP, scheduled remaining features for V1.1."
        )
    else:
        return (
            f"### Mock Interview Prep: {job_title}\n\n"
            f"**Question 1 (Core Competency)**: What do you consider the most critical skill for a successful {job_title}, and how do you demonstrate it?\n"
            f"- *Ideal Answer Structure*: Identify a key skill (e.g., communication, analysis, problem-solving). Give a concrete example of using it in a past role to drive success.\n\n"
            f"**Question 2 (Behavioral)**: Describe a challenging project you worked on and how you overcame obstacles.\n"
            f"- *Ideal Answer Structure (STAR)*: Detail the project parameters, the specific challenge (resource constraints, tight deadlines, shifting requirements), your actions to address the blocker, and the positive outcome."
        )


if __name__ == "__main__":
    # FastMCP uses sys.argv by default, but to ensure stdio runs correctly, run mcp
    mcp.run()
