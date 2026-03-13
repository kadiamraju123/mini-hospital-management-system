
Mini Hospital Management System

Run Backend:
cd hms_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Run Email Service:
cd email_service
npm install
serverless offline
