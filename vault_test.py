from settings import settings
from db_vault import get_vault_token, get_login_from_vault
from db_ops import get_football_teams
import logging
import sys
from datetime import datetime
from psycopg2 import OperationalError
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_teams(db_user, db_pw):
    logger.info(f"Getting team data at {datetime.now()}")
    team_info = get_football_teams(user=db_user, passwd=db_pw)
    for team in team_info:
        print(f"\t{team['city']} {team['team']}")
    print("")


def main_body():
    db_user = ""
    db_password = ""
    try:
        token = get_vault_token()
        logger.info(f"Token is {token}")
        db_info = get_login_from_vault(token)
        db_user = db_info["username"]
        db_password = db_info["password"]
        logger.info(f"User name from vault is {db_user}")
    except Exception as exp:
        logger.exception(f"Authentication error: {exp}", exc_info=True)
        raise exp
    # run the query and display
    while True:
        try:
            run_teams(db_user=db_user, db_pw=db_password)
        except OperationalError as op_err:
            logger.warning(
                "Failed to connect to Postgres!  Getting a new user and trying again"
            )
            db_info = get_login_from_vault(token)
            db_user = db_info["username"]
            db_password = db_info["password"]
            logger.info(f"New user name from vault is {db_user}")
            run_teams(db_user=db_user, db_pw=db_password)
        sleep(10)


# get the vault credentials
tries = 1
while tries <= 3:
    try:
        logger.info("Starting try {tries}")
        main_body()
    except Exception as exp:
        logger.error("Error occurred.  Try one more time.")
        tries += 1
