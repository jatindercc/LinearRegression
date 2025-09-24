import pandas as pd

def fetch_next_row(engine, table_name, last_id):
    print(f"📡 Fetching next row after ID {last_id}...")
    with engine.connect() as conn:
        conn.rollback()
        query = f"SELECT * FROM {table_name} WHERE id > {last_id} ORDER BY id ASC LIMIT 1;"
        df = pd.read_sql(query, conn)
        print(f"📥 Fetched {len(df)} row(s)")
        return df