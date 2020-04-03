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


# get the vault credentials
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
    logger.exception(f"Blammo: {exp}", exc_info=True)
    sys.exit(1)

# run the query and display
run_ctr = 0
while run_ctr < 15:
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
    run_ctr += 1
    sleep(10)
sys.exit(0)
