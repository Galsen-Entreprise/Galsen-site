echo " MAKE BUILDS..."
python3.9 -m ensurepip
python3.9 -m pip install -r requirements.txt
python3.9 install collectstatic

echo " MAKE MIGRATIONS..."
python3.9 manage.py makemigrations 
python3.9 manage.py migrate
python3.9 manage.py collectstatic 
