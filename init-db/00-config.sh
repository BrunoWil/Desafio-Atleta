#!/bin/sh

# Libera acesso externo ao PostgreSQL
echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"

# Permite conexões externas com autenticação md5
echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
