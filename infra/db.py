import logging

from sqlalchemy import create_engine, text
from sqlalchemy_utils import create_database, database_exists

from configs import db

logger = logging.getLogger(__name__)

engine = create_engine(db.configs.connection_string)

if not database_exists(engine.url):
    create_database(engine.url)
    logger.info("Database created")


def check_health() -> bool:
    """Check the health of the database"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
