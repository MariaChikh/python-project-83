from psycopg2.pool import SimpleConnectionPool

from page_analyzer.settings import DATABASE_URL

pool = SimpleConnectionPool(1, 10, DATABASE_URL)