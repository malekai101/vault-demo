#!/usr/bin/env bash

vault auth enable userpass >/dev/null 2>&1
vault write auth/userpass/users/vault_demo password="password" policies="pg_ro"

vault policy write secret-reader - <<- EOH > /dev/null 2>&1
    path "database/roles/football-reader" {
        capabilities = ["create", "update"]
    }
EOH

vault secrets enable database
vault write database/config/vault_demo \
     plugin_name=postgresql-database-plugin \
     connection_url="postgresql://{{username}}:{{password}}@127.0.0.1:5432/postgres?sslmode=disable" \
     allowed_roles=football-reader \
     username="root" \
     password="rootpassword"
vault write database/roles/football-reader \
      db_name=vault_demo \
      creation_statements=@readonly.sql \
      default_ttl=5m \
      max_ttl=24h

