import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:example@localhost/applepy?charset=utf8mb4"
)
