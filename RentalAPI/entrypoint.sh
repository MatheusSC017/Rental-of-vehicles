#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MySQL started"
fi

access_token=$(python create_access_token.py)
export COORDINATES_API_KEY=$access_token

python manage.py flush --no-input
python manage.py migrate
if [ "$INITIAL_DATA" = "True" ]
then
  echo "Waiting for the initial data generator..."

  python fake_data_generator.py

  echo "Generated data"
fi

exec "$@"
