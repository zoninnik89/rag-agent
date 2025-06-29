import os
import pandas as pd
from sqlalchemy import create_engine, text


def query_cloudsql(query: str) -> str:
    """
    Run a SQL query on a Cloud SQL instance and return the first few rows as markdown.

    Args:
        query (str): The SQL query to run

    Returns:
        str: Query result as markdown
    """
    user = os.environ.get("CLOUDSQL_USER")
    password = os.environ.get("CLOUDSQL_PASSWORD")
    host = os.environ.get("CLOUDSQL_HOST")  # IP address
    port = os.environ.get("CLOUDSQL_PORT", "5432")
    dbname = os.environ.get("CLOUDSQL_DB")

    connection_str = f"postgresql+pg8000://{user}:{password}@{host}:{port}/{dbname}"

    try:
        engine = create_engine(connection_str)
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
            if df.empty:
                return "Query executed successfully, but no data was returned."
            return df.head(10).to_markdown(index=False)
    except Exception as e:
        return f"Failed to run query: {str(e)}"