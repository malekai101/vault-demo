from settings import settings
import logging
import requests

logger = logging.getLogger(__name__)


def get_vault_token(vault_base_url=None) -> str:
    if vault_base_url is None:
        vault_base_url = settings["vault_url"]
    auth_url = f"{vault_base_url}/v1/auth/userpass/login/{settings['vault_user_creds']['username']}"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    body = {"password": settings["vault_user_creds"]["password"]}
    try:
        resp = requests.post(auth_url, headers=headers, json=body)
        resp.raise_for_status()
        payload = resp.json()
        if "auth" in payload:
            return payload["auth"]["client_token"]
        else:
            raise Exception("No auth section in vault return.")
    except Exception as exp:
        logger.exception(f"Failed to get a vault user token: {exp}")
        raise exp


def get_login_from_vault(token=None) -> dict:

    # pull info from settings and build url for vault
    vault_base_url = settings["vault_url"]
    if token is None:
        token = get_vault_token()
    db_cred_url = f"{vault_base_url}/v1/database/creds/football-reader"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Vault-Token": token,
    }
    try:
        resp = requests.get(db_cred_url, headers=headers)
        resp.raise_for_status()
        payload = resp.json()
        if "data" in payload:
            return payload["data"]
        else:
            raise Exception("data section missing from credentials return.")
    except Exception as exp:
        logger.exception(f"Failed to get database login info from vault: {exp}")
