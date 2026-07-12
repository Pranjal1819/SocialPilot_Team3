from sqlalchemy import create_engine, text
from app.core.config import settings

print("=" * 50)
print("SocialPilot Database Connection Test")
print("=" * 50)

try:
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("✅ PostgreSQL Connected Successfully!")

except Exception as e:
    print("❌ Database Connection Failed!")
    print(e)

print("=" * 50)