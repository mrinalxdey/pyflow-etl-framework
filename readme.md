# PyFlow ETL Framework

A configurable Python-based ETL (Extract, Transform, Load) framework that processes data from multiple file formats and loads it into a relational database. The framework supports automated file monitoring, data validation, transformations, chunked processing, and structured logging.

---

## Features

- Extract data from:
  - CSV (`.csv`)
  - Excel (`.xlsx`, `.xls`)
  - JSON (`.json`)
  - JSON Lines (`.jsonl`)
  - Parquet (`.parquet`)
  - Compressed files (`.zip`, `.gz`)
- Recursive file discovery
- Automatic directory skipping
- Data validation and cleaning
- Pandas-based transformations
- Chunked processing for large datasets
- Database loading using SQLAlchemy
- Configurable through YAML configuration files
- Structured logging
- Custom exception handling
- File watcher for automatic processing of new files
- Execution time tracking using decorators

---

## Project Structure

```text
.
├── pyflow/
│   ├── analysis/
│   │   ├── analysis.ipynb
│   │   └── analysis.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   └── logging_config.py
│   ├── logs/
│   ├── tests/
│   ├── __init__.py
│   ├── extractors.py
│   ├── loaders.py
│   ├── main.py
│   ├── transformers.py
│   ├── utils.py
│   ├── validators.py
│   └── watcher.py
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Requirements

- Python 3.10+
- PostgreSQL or MySQL
- pip

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mrinalxdey/pyflow-etl-framework.git
cd pyflow-etl-framework
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
DB_USERNAME=your_username
DB_PASSWORD=your_password
```

An example file is provided:

```text
.env.example
```

---

## Configuration

Edit the configuration file:

```text
pyflow/config/config.yaml
```

Example:

```yaml
database:
  driver: postgresql+psycopg2
  host: localhost
  port: 5432
  db_name: pyflow_etl

etl:
  chunk_size: 10000
```

For MySQL:

```yaml
database:
  driver: mysql+pymysql
  host: localhost
  port: 3306
  db_name: pyflow_etl
```

---

## Running the ETL Pipeline

Run the pipeline once:

```bash
python -m pyflow.main
```

The pipeline will:

1. Discover supported files
2. Extract data
3. Validate records
4. Apply transformations
5. Load data into the configured database
6. Log successes and failures

---

## Running the File Watcher

Start the file watcher:

```bash
python -m pyflow.watcher
```

The watcher continuously monitors the configured input directory and automatically processes newly added files.

---

## Running Both Separately

### Terminal 1

```bash
python -m pyflow.watcher
```

### Terminal 2

```bash
python -m pyflow.main
```

- `pyflow.main` performs a one-time ETL execution.
- `pyflow.watcher` continuously monitors for newly added files.

## Command Line Interface

Run a full ETL load:

```bash
python pyflow.py --config pyflow/config/config.yaml --mode full
```

Run an incremental ETL load:

```bash
python pyflow.py --config pyflow/config/config.yaml --mode incremental
```

Start the file watcher:

```bash
python pyflow.py --watch
```
---
## Logging

Logs are stored in:

```text
pyflow/logs/
```

Logs include:

- Pipeline start and completion
- File processing status
- Validation errors
- Transformation errors
- Database loading errors
- Execution timings

---

## Example Workflow

1. Configure the database credentials in `.env`.
2. Update `config.yaml` as required.
3. Start the watcher.
4. Place data files in the configured input directory.

```bash
python -m pyflow.watcher
```

Or execute a one-time run:

```bash
python -m pyflow.main
```

5. Verify logs and database tables after processing completes.

---

## Authors

**Mrinal Dey**
