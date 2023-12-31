# Wikipedia Information Retrieval System Project

A simple information retrieval system for Wikipedia articles with AI powered support.

## Introduction

This project is a simple information retrieval system for Wikipedia articles. It is written in Python 3.10 and uses cosine similarity to rank the articles. The system is able to index the articles and search for them. The search results are ranked by their cosine similarity to the query. The system is able to handle multiple queries at once and can be used in streamlit web app.

## Features

- [x] Debug mode (Prints the query and the results as well of similarity scores)

- [x] Enable AI powered support your search

## Requirements

- Docker or Docker-Compose
- Ollama
  - Your favorite llm (eg. llama2)

## Installation

1. Clone the repository

```bash
git clone https://github.com/112523chen/wikipedia-search-engine-web-app.git
cd wikipedia-search-engine-web-app
```

2. Run the docker-compose file

```bash
docker-compose up
```

You can change the environment variables in the docker-compose file

```yaml
environment:
  - OLLAMA_HOST=ollama # The hostname of the ollama server
  - OLLAMA_PORT=11434 # The port of the ollama server
  - OLLAMA_MODEL=llama2 # The model of the ollama server
```

3. Open your browser and go to http://localhost:1234

## Usage

1. Enter your query in the search bar and click search

## Setbacks

- The current system of AI powered support is not very good. It a fairly slow process. Need to find a better way to do it.
- The corpus is not very big as it as around 15000 articles. This is due to the limits that Github has on the file size. (Email me if you want the full corpus)
