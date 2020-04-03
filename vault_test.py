from settings import settings
from db_vault import get_vault_token, get_login_from_vault
from db_ops import get_football_teams
import logging
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# get the vault credentials
try:
    token = get_vault_token()
    logger.info(f"Token is {token}")
    db_info = get_login_from_vault(token)
    logger.info(f"User name from vault is {db_info['username']}")
except Exception as exp:
    logger.exception(f"Blammo: {exp}", exc_info=True)
    sys.exit(1)

# run the query and display
logger.info(f"Getting team data at {datetime.now()}")
team_info = get_football_teams(user=db_info["username"], passwd=db_info["password"])
for team in team_info:
    print(f"{team['city']} {team['team']}")
