import psycopg2.extras
from settings import settings
import logging

logger = logging.getLogger(__name__)


def get_football_teams(user: str, passwd: str) -> dict:
    postgres_settings = ["postgres_host", "postgres_port", "postgres_database"]
    if not all(
        [x in settings.get("postgres_settings", {}).keys() for x in postgres_settings]
    ):
        raise Exception("Config data for postgres is missing.")
    conn_dict = {
        "dbname": settings["postgres_settings"]["postgres_database"],
        "host": settings["postgres_settings"]["postgres_host"],
        "port": settings["postgres_settings"]["postgres_port"],
        "user": user,
        "password": passwd,
    }
    try:
        with (psycopg2.connect(**conn_dict)) as conn:
            conn.autocommit = True
            with (
                conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            ) as curr:  # type: psycopg2.extras.DictCursor
                curr.execute(
                    "select city, team_name, random() as num from tb_football_teams order by num limit 5"
                )
                rows = curr.fetchall()
                ret_dict = {}
                for row in rows:
                    ret_dict["city"] = str(row["city"])
                    ret_dict["team"] = str(row["team_name"])
                return ret_dict
    except Exception as exp:
        logger.exception(f"Meltdown in postgres code: {exp}")
        raise exp
