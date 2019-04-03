release: python3 Conet/manage.py makemigrations posting
release: python3 Conet/manage.py makemigrations Accounts
release: python3 Conet/manage.py makemigrations
release: python3 Conet/manage.py migrate
web: gunicorn --pythonpath Conet/ Conet.wsgi
