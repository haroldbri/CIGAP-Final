set -o errexit 

pip install -r requirements.txt

python crear_super.py
python crear_grupos.py

python manage.py collectstatic --no-input
python manage.py migrate