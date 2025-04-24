"""
dependencies.py
This module imports all the necessary libraries required for the project.
"""

import psycopg2
import pandas as pd
import yaml as yaml
from dotenv import load_dotenv
import os
import io as io
from datetime import datetime, timezone
import logging as logging

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using environment variables.
    Returns:
        psycopg2 connection object
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )