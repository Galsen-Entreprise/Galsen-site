pip install -r requirements.txt
python3.7 install collectstatic
python3.7 manage.py makemigrations --noinput
python3.7 manage.py migrate --noinput
python3.7 manage.py collectstatic --noinput --clear