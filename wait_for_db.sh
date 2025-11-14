#!/bin/sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

while ! nc -z $host $port; do
    echo "Waiting for PostgreSQL ($host:$port)..."
    sleep 2
done

echo "PostgreSQL is up - executing command"

exec $cmd