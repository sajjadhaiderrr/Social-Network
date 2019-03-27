release: python3 Conet/manage.py makemigrations posting
release: python3 Conet/manage.py makemigrations Accounts
release: python3 Conet/manage.py migrate
web: gunicorn Conet.Conet.wsgi
