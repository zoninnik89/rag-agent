# RAG Agent — Vertex AI + Cloud SQL + Gemini Agent

A structured Gemini-based agent that supports both **document-based RAG queries** and **SQL table queries** via natural language.

---

## Features

* **Retrieval-Augmented Generation (RAG)** via Vertex AI
* Manage corpora: upload, list, delete
* Run **natural language questions** over a PostgreSQL **Cloud SQL** database
* Gemini 2.5-powered agent with multi-tool reasoning

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/zoninnik89/rag-agent.git
cd rag-agent
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Authenticate with Google Cloud

Ensure you’ve authenticated with your GCP account:

```bash
gcloud auth application-default login
```

This allows access to Vertex AI and Cloud SQL.

### 5. Prepare Environment Variables

Create a `.env` file in the root directory with the following structure:

```ini
PROJECT_ID={gcp_project_id}
LOCATION=us-central1

# Cloud SQL access
DB_HOST={ip_address}
DB_PORT=5432
DB_NAME=test_db
DB_USER=test_user
DB_PASSWORD=your_password
```

> Make sure `DB_HOST` points to an accessible Cloud SQL instance (public IP or localhost if port forwarded).

---

## Quick Start

Once everything is set up, you can run the agent directly:

```
Run "adk web" in the IDE terminal and it will bring up a web server on your local machine with a Web GUI to run queries.
```

---

## Available Tools

| Tool              | Description                                  |
| ----------------- | -------------------------------------------- |
| `rag_query`       | Query current document corpus                |
| `add_data`        | Add Google Drive / GCS files to corpus       |
| `create_corpus`   | Create a new document corpus                 |
| `list_corpora`    | Show all existing corpora                    |
| `get_corpus_info` | Inspect a specific corpus                    |
| `delete_document` | Delete individual document from corpus       |
| `delete_corpus`   | Delete entire corpus                         |
| `query_cloudsql`  | Run natural language SQL over `orders` table |

---

## SQL Schema Assumed

The agent assumes a table like this exists:

```sql
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  customer_id TEXT NOT NULL,
  order_date DATE,
  total_amount FLOAT,
  status TEXT
);
```

---

## Project Structure

```
rag-agent/
├── src/
│   ├── agent.py               # Root Gemini agent with tools
│   └── tools/                 # RAG + SQL tool definitions
├── requirements.txt
├── .env.example               # Sample env config
└── README.md
```

---

## Sample Questions You Can Ask

```
Show all orders from June
What is the status of order #102?
List all orders where total_amount > 200
How many orders are marked as 'shipped'?
```

---

## License

MIT License © [zoninnik89](https://github.com/zoninnik89)
