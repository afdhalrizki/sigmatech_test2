# TEST 2 SIGMATECH
## PROGRAM REQUIREMENTS:
- Python (Djange, celery, flower)
- Redis for windows
- Mongodb desktop

## HOW TO RUN PROGRAM:
Django:
```bash
python manage.py runserver
```
Celery worker:
```bash
celery -A restapi.celery worker --pool=solo -l info
```
Celery flower:
```bash
celery -A restapi flower --port=5566 --broker=redis://redis:6379/0
```

## TESTING PROGRAM WITH POSTMAN:
### 1. Register:
- **POST** localhost:8000/register/
- No Authentication
- Fields: phone_number, password, confirm_password, first_name, last_name, address

### 2. Login:
- **POST** localhost:8000/login/
- No Authentication
- Fields: phone_number, password

### 3. Showing Profile:
- **GET** localhost:8000/profile/
- Token Authentication
- No Fields

### 4. Update Profile:
- **PUT** localhost:8000/profile/
- Token Authentication
- Fields: first_name, last_name, address

### 5. Top Up
- **POST** localhost:8000/topup/
- Token Authentication
- Fields: amount_to_up

### 6. Payment 
- **POST** localhost:8000/pay/
- Token Authentication
- Fields: amount, remarks

### 7. Transfer
- **POST** localhost:8000/transfer/
- Token Authentication
- Fields: amount, remarks, target_user

## FLOWER DASHBOARD:
```bash
http://localhost:5566/tasks
```
