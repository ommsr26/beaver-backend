from sqlalchemy import text
from sqlalchemy.engine import Engine
from datetime import datetime

def get_monthly_usage(engine: Engine):
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    query = text("""
        SELECT 
            api_key,
            COUNT(*) AS request_count
        FROM usage_logs
        WHERE created_at >= :month_start
        GROUP BY api_key
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"month_start": month_start})
        return {row.api_key: row.request_count for row in result}
