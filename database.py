import sqlite3

from sqlalchemy import create_engine, StaticPool

engine = create_engine("sqlite:///storage/vidpro.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)
