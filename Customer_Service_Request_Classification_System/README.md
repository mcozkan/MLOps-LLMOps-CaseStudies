# AI-Powered Customer Request Classification System

This project classifies customer support requests by category, priority, tags, and estimated resolution time using LangChain, structured LLM outputs, SQLModel, and PostgreSQL.

Customer support teams receive requests from multiple channels such as email, chat, and web forms. Manually categorizing and prioritizing these requests is time-consuming and error-prone.

This project automates the classification of customer requests by extracting structured information such as category, priority, tags, and estimated resolution time.

## Scope

This project includes:

- Reading customer request data from CSV
- Processing each request individually
- Classifying requests using an LLM
- Storing raw requests and classification results in PostgreSQL
- Querying results through SQL joins
- Handling invalid inputs and API/database errors

This project does not include:

- Real-time message queue processing
- Frontend dashboard
- Multi-user authentication
- Batch optimization for high-volume production traffic

## Features

- CSV-based customer request ingestion
- LangChain-powered request classification
- Structured output validation
- PostgreSQL database persistence
- SQLModel-based schema design
- Two-table relational database structure
- Error handling for invalid inputs and API failures
- Modular Python codebase

## Tech Stack

- Python
- Pandas
- LangChain
- Google Gemini AI
- SQLModel
- PostgreSQL
- Docker
- DVC

## Project Structure

```text
customer_service_project/
│
├── data/
│   ├── raw/
│       ├── sample_requests.csv
│   ├── processed/
│
│── artifacts/
│   ├── reports/
│       ├── ticket_created_log_report.txt
│   ├── screenshots/
│       ├── DbTables_ss.png
│       ├── table_check_0.png
│       ├── table_check_1.png 
│
├── src/
│   ├── main.py
│   ├── db_operations.py
│   ├── models.py
│
├── docker-compose.yaml
├── requirements.txt
├── .gitignore
├── README.md
└── dvc.yaml
```
The project follows a modular architecture.

## Processing Workflow

```text
sample_requests.csv
        ↓
pandas DataFrame
        ↓
Single-row processing loop
        ↓
LangChain Agent
        ↓
Google Gemini AI
        ↓
Structured Pydantic Output
        ↓
PostgreSQL Database
 ├── customer_requests
 └── request_classifications
```

## Database Design

The database contains two main tables:

### customer_requests

Stores raw customer request data.

| Column | Description               |
|---|---------------------------|
| id | primary key               |
| ticket_id | Unique request identifier |
| customer_id | Customer identifier       |
| channel | Source channel            |
| request_text | Original customer message |
| created_at | request time created      |

### request_classifications

Stores LLM-generated classification results.

| Column                    | Description                             |
|---------------------------|-----------------------------------------|
| id                        | primary key                             |
| ticket_id                 | Foreign key linked to customer_requests |
| category                  | Classified request category             |
| priority                  | Priority level                          |
| tags                      | Extracted tags                          |
| estimated_resolution_time | Estimated handling time                 |
| confidence                | Classification confidence score         |
| processed_at                | request processed time                  |


The two-table structure separates raw input data from generated classification results. This improves traceability, enables auditing, and prevents overwriting original customer messages.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd customer_service_project
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. configure Environment Variables

```bash
DATABASE_URL=postgresql://admin:admin@localhost:5433/customer_service_db
GOOGLE_API_KEY=your_google_gemini_api_key
```
#### Never and ever send the .env file to GitHub.

## Docker Setup

```bash
# Running with Docker:
docker compose up -d

# check running containers:
docker ps

# Connect to PostgreSQL:
docker exec -it postgres_db psql -U admin -d customer_service_db
```

![Database Tables](artifacts/screenshots/DbTables_ss.png)

## Running App
```bash
python src/main.py
```

## Example Output:
```bash
{
  "category": "billing",
  "priority": "high",
  "tags": ["duplicate_charge", "payment_issue"],
  "estimated_resolution_time": 24,
  "confidence": 0.91
}
```
## Processing Report

A detailed processing log is stored under:

```text
artifacts/reports/ticket_created_report.txt
```

## Example SQL Query

```sql
SELECT
    cr.ticket_id,
    cr.customer_id,
    cr.channel,
    rc.category,
    rc.priority,
    rc.tags,
    rc.estimated_resolution_time,
    rc.confidence
FROM customer_requests cr
JOIN request_classifications rc
ON cr.ticket_id = rc.ticket_id;
```
![Database Tables](artifacts/screenshots/table_check_1.png)

```sql
SELECT cr.ticket_id
FROM customer_requests cr
LEFT JOIN request_classifications rc
ON cr.ticket_id = rc.ticket_id
WHERE rc.ticket_id IS NULL;
```
![Database Tables](artifacts/screenshots/table_check_0.png)

This query shows that the system correctly connects both tables.

## Configuration in .env 

Main configuration values are managed through environment variables:

| Variable | Description |
|---|---|
| DATABASE_URL | PostgreSQL connection string |
| GOOGLE_API_KEY | Google Gemini API key |

## Data Versioning with DVC

This project uses DVC to track data files without storing large datasets directly in Git.

```bash
# Pull data files:
dvc pull

# Track data changes:
dvc add data/sample_requests.csv
```

## Evaluation Criteria Mapping

| Requirement | Status |
|---|-|
| CSV processing with pandas | OK |
| LangChain agent integration | OK |
| Gemini AI classification | OK |
| Structured output validation | OK |
| PostgreSQL integration | OK |
| Two-table relational schema | OK |
| Error handling | OK |
| Single request processing loop | OK |



## API Rate Limit Handling & Retry Strategy

The project includes retry-based API error handling using `tenacity`.

If the Gemini API temporarily fails or reaches quota limits:

- The system retries failed requests automatically
- Waits between retry attempts
- Prevents full pipeline crashes
- Continues processing remaining tickets

The project also includes a real execution log demonstrating:

- Gemini API quota exhaustion (`HTTP 429 RESOURCE_EXHAUSTED`)
- Automatic retry behavior using `tenacity`
- Exception handling with traceback logging
- Pipeline continuation without full application crash

This demonstrates robust API failure handling and resilient row-by-row processing behavior.

Example report:

```text
artifacts/reports/ticket_created_log_report_09052026.txt
```


## Known Limitations

- The current version processes requests sequentially.
- It does not include asynchronous batch processing.
- Classification quality depends on the LLM response.
- No frontend dashboard is included yet.
- Large-scale production deployment would require queue-based processing and monitoring.

## Future Improvements

- Add FastAPI endpoints
- Build a Streamlit or web dashboard
- Add async request processing
- Add monitoring with Grafana
- Add more integration tests
- Add authentication and user roles
- Improve prompt evaluation and classification metrics
