#!/usr/bin/env bash

docker exec -i vault-demo-postgres psql -U root -c "CREATE DATABASE vault_demo;"
docker exec -i vault-demo-postgres psql -U root -d vault_demo -t < pg_configure.sql