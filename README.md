# Diego Vegas - Portfolio

Personal portfolio and showcase of selected software projects.

The website contains information about my work, projects and technical interests.

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

Retrieval-Augmented Generation (RAG) project.

The engine answers natural language questions using relevant extracts from a text source. Powered by OpenAI embeddings, it uses cosine similarity to retrieve the most relevant text fragments and generate responses.

**Technologies:** Python, OpenAI API

→ `/lecter`

## Website

The portfolio itself is intentionally built without a web framework.

It uses a custom HTTP server written in Python to handle requests, routing and static files. The goal was to keep the underlying implementation simple and transparent rather than relying on a framework.

    Browser
       ↓
    HTTP request
       ↓
    Custom Python server
       ↓
    Routing / static files
       ↓
    HTML / CSS / project pages

## Structure

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

## Deployment

The website is deployed using Railway and runs the same Python server used during local development.

The project is served from:

**https://diegovegas.de**

## About

I'm Diego Vegas, a Computer Engineering student interested in software engineering, backend development, data and artificial intelligence.

This repository contains the code behind my personal portfolio as well as selected projects that I use to experiment with different areas of software development.
