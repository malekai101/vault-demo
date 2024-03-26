# Installation

This file contains the installation instructions for the demo.  All instructions are for a Mac with python 3.11 
installed through Brew.

## Python - Run in project root

* Pull the code from Github into a working directory.
* Install a python 3.11 virtual environment: `python3.11 -m venv venv`
* Activate the venv: `source env/bin/activate`
* Install the packages: `pip install -r requirements.txt`

## Postgres - run in Installation

* Start postgres in docker: `docker run --name vault-demo-postgres -p 5432:5432 -e POSTGRES_USER=root  -e POSTGRES_PASSWORD=rootpassword -d postgres`
* Run the postgres configuration script: `./pg_setup.sh`

## Vault - run in Installation

* Start a local vault server: `vault server -dev -dev-root-token-id="root"`
* Set local Vault environmental variables: 
  * `export VAULT_ADDR="http://127.0.0.1:8200`
  * `export VAULT_TOKEN="root"`
* Run the Vault setup script: `./vault_setup.sh`