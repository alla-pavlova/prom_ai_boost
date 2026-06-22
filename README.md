# Prom AI Boost

AI-powered CLI tool for automated Prom.ua product content generation using Excel, OpenAI API and structured JSON workflows.

## Features

* Import products from Excel (.xlsx)
* Generate product descriptions in Ukrainian and Russian
* Generate HTML descriptions for Prom.ua
* Generate SEO tags
* Strict JSON responses from OpenAI
* Duplicate SKU detection
* Product processing statuses
* Processing timestamps
* OpenAI token usage tracking
* Estimated API cost calculation
* Source Facts JSON layer
* Local cache system
* Cache usage statistics
* Processing logs
* Error export to a separate Excel file
* Versioned output files

## Processing Flow

Excel → Source Facts (JSON) → Cache → OpenAI → JSON Response → Output.xlsx

## Statuses

* processed
* duplicate
* skipped
* error
* no_data

## Tech Stack

* Python 3.10
* OpenAI API
* Pandas
* OpenPyXL
* Python Dotenv

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
USE_OPENAI=true
OPENAI_API_KEY=your_api_key

INPUT_FILE=data/input.xlsx
OUTPUT_FILE=data/output.xlsx

MODEL=gpt-4o-mini

OPENAI_INPUT_PRICE_PER_1M=0.15
OPENAI_OUTPUT_PRICE_PER_1M=0.60

USE_WEB_SEARCH=false
SEARCH_PROVIDER=mock
CACHE_DIR=cache
```

## Run

```bash
python -m app.main
```

## Output

The generated Excel file contains:

* description_ua
* description_ru
* html_description
* seo_tags
* status
* error_message
* processed_at
* source_facts
* tokens_used
* estimated_cost_usd

## Current Version

### v0.5

✔ OpenAI integration
✔ JSON responses
✔ Token usage tracking
✔ Cost estimation
✔ Source Facts architecture
✔ Local cache system
✔ Cache statistics
✔ Duplicate SKU detection
✔ Error reports
✔ Versioned output files

## Roadmap

### v0.6

* Web Search integration
* Serper API support
* Anti-hallucination workflow

### v0.7

* XML import/export

### v0.8

* Prom.ua characteristics mapping

### v0.9

* FastAPI API

### v1.0

* Telegram Bot

### v1.1

* SQLite storage

### v1.2

* Automated tests

### v2.0

* Web SaaS platform

```
```
