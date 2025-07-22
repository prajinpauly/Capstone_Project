# Aged Care & Disability HRM Chatbot

## Overview

This project is an intelligent conversational agent designed to streamline information gathering and compliance checks for organizations in the aged care and disability sector. Built using advanced language models (OpenAI GPT via LangChain) and a step-by-step guided questioning workflow, the chatbot automates the collection of HRM and regulatory data, helping providers close compliance gaps and improve operational efficiency.

---

## Objectives

- Automate the collection of HRM and compliance information from aged care/disability service providers.
- Guide users through a structured, step-by-step interview to ensure all regulatory and operational requirements are addressed.
- Export collected data for further analysis, reporting, or audit purposes.
- Lay the foundation for future integration with databases, analytics, or dashboarding tools.

---

## Real-World Relevance

- **Compliance:** Ensures organizations gather all required information for NDIS, Aged Care Quality Standards, and other regulations.
- **Efficiency:** Reduces manual paperwork and repetitive data entry for HR and compliance teams.
- **Audit Readiness:** Provides a clear, exportable record of all responses for internal or external review.
- **Scalability:** Can be extended to other regulated industries or integrated with existing HRM systems.

---

## Key Features

- **Conversational Workflow:** Guides users through 15 essential HRM and compliance questions.
- **Memory Buffer:** Remembers previous answers to maintain context in multi-turn conversations.
- **CSV Export:** Automatically saves all Q&A to a CSV file for easy reporting.
- **Customizable:** Easily adapt the question set or workflow for other industries or requirements.
- **API Ready:** Flask-based backend for easy integration with web or mobile frontends.

---

## Example Questions

1. What is the name of your aged care or disability service?
2. Can you describe the main services you provide?
3. Who are your primary clients (e.g., elderly, people with disabilities)?
4. What are the key HR challenges you face (e.g., staff shortages, training, compliance)?
5. Are there specific regulatory requirements you must comply with (e.g., NDIS, Aged Care Quality Standards)?
6. What systems do you currently use for HR management (e.g., rostering, payroll, training)?
7. Do you have issues with staff retention or recruitment?
8. What are your main concerns regarding staff training and qualifications?
9. How do you currently track compliance and incident reporting?
10. Are there any technology gaps in your current HRM processes?
11. What is your preferred method for staff communication and updates?
12. Do you require integration with existing HR or care management systems?
13. What is your desired timeline for improving your HRM processes?
14. Are there any key milestones or audits coming up?
15. Is there any other information about your HRM needs or regulatory requirements?

---

## Technology Stack

- **Backend:** Python, Flask, LangChain, OpenAI GPT (Azure)
- **Data Handling:** pandas, CSV export
- **Session Management:** Flask-Session
- **(Optional):** MySQL for persistent storage

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/aged-care-hrm-chatbot.git
cd aged-care-hrm-chatbot
