import pandas as pd
from sqlalchemy import create_engine

DB_CONFIG = {
    "host": "ep-patient-rice-abq9p7gq-pooler.eu-west-2.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_acXRFH87rmsN",
    "port": "5432",
    "sslmode": "require",
}

def connect_to_db():
    url = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?sslmode={DB_CONFIG['sslmode']}"
    return create_engine(url)

def load_csv_to_db_old(csv_path, engine, table_name='cat_dataset'):
    df = pd.read_csv(csv_path)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "id"}, inplace=True)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅ Loaded {len(df)} rows into '{table_name}'")

def load_csv_to_db(csv_path, engine, table_name='cat_dataset'):
    df = pd.read_csv(csv_path)

    # Convert Time column to proper datetime format
    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], errors='coerce')

    # Ensure column order matches DB schema
    expected_cols = ["Trait"] + [f"Axis #{i}" for i in range(1, 15)] + ["Time"]
    df = df[[col for col in expected_cols if col in df.columns]]

    # Save to DB
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅ Loaded {len(df)} rows into '{table_name}'")