# SocialPilot Backend

FastAPI + PostgreSQL backend for SocialPilot.

## Database Setup

1. Install PostgreSQL and create a database named `socialpilot_db`
2. Copy `.env.example` to `.env` and fill in your database credentials
3. Activate virtual environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `alembic upgrade head`
6. Verify connection: `python test_db.py`

## Tables

- `users` — user accounts
- `scheduled_posts` — individual scheduled content
- `campaigns` — grouped marketing campaigns
- `post_analytics` — engagement metrics per post/campaign

## Schema Details

Full column definitions and relationships are in `models.py`. 
Table creation is managed via Alembic migrations in the `alembic/` folder.