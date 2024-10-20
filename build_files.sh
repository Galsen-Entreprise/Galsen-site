echo " MAKE BUILDS..."
pip install -r requirements.txt
python3.7 install collectstatic

echo " MAKE MIGRATIONS..."
python3.7 manage.py makemigrations 
python3.7 manage.py migrate
python3.7 manage.py collectstatic 
