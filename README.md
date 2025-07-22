# Aged Care & Disability HRM Recruiter Chatbot

## Overview

This project is an intelligent conversational agent designed to streamline candidate screening, HR data collection, and compliance checks for recruiters and HR professionals in the aged care and disability sector. Built using advanced language models (OpenAI GPT via LangChain) and a structured, step-by-step workflow, the chatbot automates the gathering of essential information, helping organizations close compliance gaps and improve hiring efficiency.

The system is extensible, supports CSV export for reporting, and can be integrated with web frontends or other business tools.

---

## Objectives

- Automate the collection of candidate and HRM information for recruitment in aged care/disability services.
- Guide recruiters and candidates through a structured, step-by-step interview to ensure all regulatory and operational requirements are addressed.
- Export collected data for further analysis, reporting, or audit purposes.
- Lay the foundation for future integration with databases, analytics, or dashboarding tools.

---

## Real-World Relevance

- **Recruitment Efficiency:** Streamlines the initial screening and data collection process for recruiters.
- **Compliance:** Ensures all required information for NDIS, Aged Care Quality Standards, and other regulations is gathered.
- **Audit Readiness:** Provides a clear, exportable record of all responses for internal or external review.
- **Scalability:** Can be extended to other regulated industries or integrated with existing HRM and ATS systems.

---

## Key Features

- **Conversational Workflow:** Guides users through essential HRM and recruitment questions.
- **Memory Buffer:** Remembers previous answers to maintain context in multi-turn conversations.
- **CSV Export:** Automatically saves all Q&A to a CSV file for easy reporting.
- **Customizable:** Easily adapt the question set or workflow for other industries or requirements.
- **API Ready:** Flask-based backend for easy integration with web or mobile frontends.

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
git clone https://github.com/yourusername/aged-care-hrm-recruiter-chatbot.git
cd aged-care-hrm-recruiter-chatbot
