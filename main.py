import streamlit as st
from utils.db_connection import init_db

init_db()
st.title("Cricbuzz LiveStats - Created by Anuradha Menon")
st.write("Welcome to the cricket analytics dashboard!")
st.write("Use the sidebar to navigate to Live Matches, Top Stats, SQL Analytics, or CRUD Operations.")
