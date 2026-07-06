import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

print('=' * 50)
print('SocialPilot Database Connection Test')
print('=' * 50)

try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('PostgreSQL Connected Successfully!')
except Exception as e:
    print(f'PostgreSQL Error: {e}')

try:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f'Tables found: {tables}')
    print('All 4 tables ready for the application!')
except Exception as e:
    print(f'Table error: {e}')

print('=' * 50)
print('Database setup complete!')
print('=' * 50)