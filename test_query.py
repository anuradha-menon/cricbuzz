from utils.db_connection import fetch_data
from sql_queries import QUERIES
for q in QUERIES:
    print(f"Q{q['id']}: {q['question']}")
    print(fetch_data(q['sql']))