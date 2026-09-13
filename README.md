
# Diego Vegas — Portfolio

Personal portfolio and showcase of selected software projects.

The website contains information about my work, projects and technical interests, with a focus on software engineering, data and artificial intelligence.

## Projects

### DABID

AI-powered data analysis and reporting platform.

DABID is designed to work with business data and allow users to ask questions in natural language. The system processes the underlying data and generates useful answers and documentation.

**Technologies:** Python, SQL, HTML, OpenAI API

→ `/dabid`

### ENTITY

Entity search engine built around a large structured dataset.

The project implements its own search and relevance-ranking system, including q-gram indexing and SQL-based querying.

**Technologies:** Python, SQL, C++

→ `/entity`

### LECTER

Retrieval Augmented Generation inspirated project

The engine answer human language questions and answer giving extracts of a text source. Powered by OPENAI embedding system,
this project uses cos-sim to get the most look alike fragments from the text to respond the query

**Technologies:** Python, OpenAI API

→ `/lecter`

## Website

The portfolio itself is intentionally built without a web framework.

It uses a custom HTTP server written in Python to handle requests, routing and static files. The goal was to keep the underlying implementation simple and transparent rather than relying on a framework.

```text
Browser
   ↓
HTTP request
   ↓
Custom Python server
   ↓
Routing / static files
   ↓
HTML / CSS / project pages
````

## Structure

```text
.
├── dabid/
│   └── index.html
├── entity/
│   ├── index.html
│   ├── qgram_index.py
│   ├── sparql_to_sql.py
│   ├── utils.py
│   └── wikidata-complex.sql
├── lecter/
│   └── index.html
├── index.html
├── server.py
└── style.css
```

## Running locally

Clone the repository:

```bash
git clone git@github-personal:kkuntav/portfolio.git
cd portfolio
```

Run the server:

```bash
python server.py
```

The portfolio will then be available locally through the configured port.

## Deployment

The website is deployed using Railway and runs the same Python server used during local development.

The project is served from:

**https://diegovegas.de**

## About

I'm Diego Vegas, a Computer Engineering student interested in software engineering, backend development, data and artificial intelligence.

This repository contains the code behind my personal portfolio as well as selected projects that I use to experiment with different areas of software development.

---

**Diego Vegas**
Software Engineering / AI

```

```
