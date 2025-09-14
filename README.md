# Cricbuzz LiveStats
A Streamlit app for cricket analytics using RapidAPI and PostgreSQL.

## Features
- Live match updates via Cricbuzz API.
- Player stats (ODI, Test, T20).
- 25 SQL queries for analytics (Beginner, Intermediate, Advanced).
- CRUD operations for player/match data.

## Setup
1. Install Python 3.8+ and PostgreSQL.
2. Create `.env` with:
3. Run `pip install -r requirements.txt`.
4. Initialize DB: `python init_db.py`.
5. Populate data: `python populate_db.py`.
6. Start app: `streamlit run main.py`.
7. Open `http://localhost:8501`.

## Dependencies
- streamlit
- psycopg2-binary
- pandas
- requests
- python-dotenv

## Notes
- Test player IDs in RapidAPI dashboard.
- Add more data to `populate_db.py` for richer query results.