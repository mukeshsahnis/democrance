![python-version](https://shields.io/badge/python-v3.10.2-blue)
![django-version](https://shields.io/badge/django-4.0-blue)

# Democrance test

- Used default sqlite3 however you can use Mysql or any DBMS
- In another DBMS you have to change the settings as describe in django-v4.0

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

## API endpoint testing

- tested on postman with content-type application/json and raw json data in request as follows:

- to test customer creation following fields are required

```json
{
  "email": "foo@gmail.com",
  "password": "democrance@123",
  "first_name": "Foo",
  "last_name": "Bar",
  "dob": "06-10-1989"
}
```

- to test quote creation following fields are required in request

```json
{
  "customer_id": "2",
  "type": "personal-accident",
  "premium": 200,
  "cover": 200000,
  "state": "new"
}
```

## Creation of quote by customer

- When customer create any quote for policy we keep it new as default to allow the user to accept the quote for live login as admin(superuser) and just change the state of policy to bounded.
- On state is changed to bounded it is visible on user dashboard to accept the quote

## Verifying things

- Just create super user with following command

```python
python manage.py createsuperuser
```

- Login /admin/ and verify the things

### Thanks a lot to read this.
