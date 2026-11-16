# Job Scanner: Smart Job Aggregator for High-Tech Internships & Juniors

This repository contains the **Job_Scanner** module I developed to **rapidly aggregate internship and junior tech roles** from multiple online job boards.

Built as part of the *InternSheep* hackathon project, this backend component was designed for **speed, scalability, and flexibility**, and optimized through **multithreading** and **caching** to reduce latency and avoid redundant requests.

---

## Core Performance Features

- **Multithreaded Fetching**: Uses Python’s `threading` to run API calls in parallel, drastically cutting total query time  
- **Local Caching**: Stores recent query results to reduce repeated network requests and improve response speed  
- **Optimized Runtime**: Can scan multiple APIs and return filtered listings in seconds, even across large datasets  

---

## Other Features

- **Keyword Filtering**: Search by title, technologies, company names, or any free-text term  
- **Location Filtering**: Support for Israel-specific, remote, or country-based queries  
- **Modular Sources**: Easily plug in or remove job APIs, web scrapers, or feeds  
- **CSV Export**: Generates a structured, sortable `.csv` file of matched listings  
- **Extendable Architecture**: Designed to integrate with additional systems (e.g., resume tailoring)

---

## Supported Job Sources

The scanner fetches listings from the following platforms via dedicated fetch functions:

- **RemoteOK**: Remote tech roles  
- **Adzuna**: Country-specific job data  
- **Remotive**: Curated remote positions  
- **Airtable (Goonzile)**: Israeli tech job board  
- **Arbeitnow**: Global listings with location filters

---

## Output Format

Job results are exported to a CSV file with the following fields:

- `Title`  
- `Link to apply`  
- `Location`  
- `Posted date`  
- `Description`  

---

## Design Decisions

To handle large-scale aggregation while keeping response time low:
- I implemented **thread-safe concurrent fetching** using Python's `threading` module
- I built a **custom caching mechanism** using query hashing and TTL logic  
Together, these improvements **reduced total runtime by over 70%** compared to sequential fetches.

---

## Project Structure


---

## Contact

For suggestions, questions, or collaboration:

- Email: yairthfc@gmail.com  
- LinkedIn: [linkedin.com/in/yairmahfud](https://www.linkedin.com/in/yairmahfud)

---

## ‍Part of the *InternSheep* Hackathon Project  
*Note: This repository includes only the backend scanner module. The full project featured a web platform and AI-powered resume tailoring.*

---

## License

This project is open-source and available for personal and educational use.

