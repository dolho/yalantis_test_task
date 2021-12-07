# Setup 
Prerequisites: 
You have installed python3.10 and pip; 

1) Execute in console 
```
git clone https://github.com/dolho/yalantis_test_task.git
cd yalantis_test_task
```
Or download the code as zip file and open the root folder of the project.

2) (Optionally) Create and start virtual environment
https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/

3) Execute in console 
```
pip install -r requirements.txt 
```

4) (Optionally) In the root directory of the project create .env file, and add following string in it
```
SECRET_KEY=your_secret_key
```
Instead of "your_secret_key", write your secret key. 
You can generate it with django https://tech.serhatteker.com/post/2020-01/django-create-secret-key/

5) Execute in console 
```
python manage.py makemigrations
python manage.py migrate
```
5) Run the application with following command:
```
python manage.py runserver
```
If port 8000 is already in use, you can run application on a different port with next command: 
```
python manage.py runserver 9999
```
Instead of 9999 you can choose any other available port 