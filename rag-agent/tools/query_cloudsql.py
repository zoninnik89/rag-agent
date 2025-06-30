import os
import pandas as pd
from google.adk.tools.tool_context import ToolContext
from sqlalchemy import create_engine, text

CLOUD_SQL_USER = os.getenv("CLOUD_SQL_USER", "postgres")
CLOUD_SQL_PASSWORD = os.getenv("CLOUD_SQL_PASSWORD", "your_password")
CLOUD_SQL_DB = os.getenv("CLOUD_SQL_DB", "postgres")
CLOUD_SQL_HOST = os.environ.get("CLOUD_SQL_HOST")  # IP address
CLOUD_SQL_PORT = os.environ.get("CLOUD_SQL_PORT", "5432")

DB_URI = (
    f"postgresql+psycopg2://{CLOUD_SQL_USER}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_HOST}:{CLOUD_SQL_PORT}/{CLOUD_SQL_DB}"
)


def query_cloudsql(query: str, tool_context: ToolContext) -> str:
    """
    Execute a SQL query (SELECT, INSERT, DELETE) on Cloud SQL using direct connection,
    and save the query and result in tool_context.state, then return the result as markdown.

    Args:
        query (str): The SQL query to run
        tool_context (ToolContext): Context of the Agent

    Returns:
        str: Query result as markdown

    """

    try:
        engine = create_engine(DB_URI)
        with engine.connect() as conn:
            result = conn.execute(text(query))
            qtype = query.strip().lower().split()[0]

            if qtype == "select":
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                if df.empty:
                    response = "Query successful, but returned no rows."
                else:
                    response = f"Query successful. Returned {len(df)} rows:\n\n" + df.to_markdown(index=False)

            elif qtype in ("insert", "delete", "update"):
                affected = result.rowcount
                response = f"{qtype.capitalize()} successful. {affected} row(s) affected."

    except Exception as e:
        response = f"Failed to run query: {e}"

    # Save to tool_context.state
    if hasattr(tool_context, "state"):
        history = tool_context.state.get("sql_query_history", [])
        history.append({
            "query": query,
            "result": response,
        })
        tool_context.state["sql_query_history"] = history

    return response
