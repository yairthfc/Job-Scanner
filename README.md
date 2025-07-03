# Intern-Sheep: Smart Job Scanner for Internships & Juniors

This repository contains the **Job_Scanner** module that programmatically queries multiple job-listing APIs, filters results based on keywords and location, and exports the listings to a CSV file.  
It features built-in **multithreading** and **caching** to optimize performance by minimizing runtime and redundant API calls.

This script was written as part of a broader **hackathon project**, where we built a web platform that:
1. **Finds job opportunities** (in Israel or worldwide) based on user-provided keywords  
2. **Tailors resumes** to match each job post, using an uploaded CV as the base template

---

## 🚀 Features
- 🔍 **Keyword filtering** – Search by role, technology, company name, or free-text terms  
- 🌍 **Location-based filtering** – Filter jobs by country, remote roles, or local (e.g., Israel)  
- ⚡ **Multithreaded fetching** – Parallel requests to reduce response time  
- 🧠 **Caching layer** – Prevents repeated requests and accelerates common searches  
- 🔧 **Modular and pluggable** – Add/remove job APIs or custom post-processing logic  
- 📤 **CSV export** – Save matched listings to a clean, sortable CSV file  

---

## 🌐 Supported Job Sources

The scanner currently fetches listings from:

- **Remotive** — Remote tech jobs (`_fetch_remotive()`)  
- **Adzuna** — Country-specific listings (`_fetch_adzuna()`)  
- **RemoteOK** — Remote positions across multiple industries (`_fetch_remoteok()`)  
- **Airtable (Goonzile)** — Israeli job aggregator (`_fetch_goonzile()`)  
- **Arbeitnow** — Global job board (`_fetch_arbeitnow()`)

---

## 📄 Output Example

For every match, the script generates a CSV file with the following columns:

- Job Title  
- Application Link  
- Location  
- Date Posted  
- Description  

---

## 🗂️ Project Structure
job_scanner.py - Main orchestration script for job search and export
job_finder.py - Fetches job data from APIs
cache_utils.py - Caching helper logic
config.py - Customizable settings and API keys
README.md - This documentation

---

## 📬 Contact & Feedback

Questions, suggestions, or bug reports? Reach out anytime:

- 📧 Email: yairthfc@gmail.com
- 🔗 LinkedIn: [https://www.linkedin.com/in/yairmahfud]

---

## 📜 License

This project is open-source and available for personal and educational use.
