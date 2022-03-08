![python-version](https://shields.io/badge/python-v3.10.2-blue)
![django-version](https://shields.io/badge/django-4.0-blue)

# Democrance test

```bash
# Clone repository
git clone https://github.com/mukeshsahnis/democrance.git
cd democrance

# creating virtual env
# python3 -m venv path/to/venv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements/requirements-dev.txt

# Create database and tables
python manage.py migrate
# Start development server
python manage.py runserver
```
