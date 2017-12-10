## Steps to setup project :-
1) git clone the project.
2) git checkout develop
3) cd team_members
4) pip install virtualenv
5) virtualenv env
6) source env/bin/activate
7) pip install -r requirements.pip
8) setup mysql server in the system with username **root** and password **qwerty**
9) log into mysql console via **mysql -uroot -pqwerty**
10) create database **team_management_system**;
11) exit mysql console by typing **exit**
12) cd team_management_system
13) There are some errors with django-logging-json module in python 2.7, which I have used. So, two files need to be edited for the code to work. The pros of django-logging-json outweigh the negatives. So, I chose to stick with this module.
14) vim ../env/lib/python2.7/site-packages/django_logging/cursor_wrapper.py. Go to line number **36**. 
Replace ***Thread(target=do_log, args=(self.cursor, *args)).start\(\)*** by ***Thread(target=do_log, args=(self.cursor, args)).start()***. Save the file and exit.
15) vim ../env/lib/python2.7/site-packages/django_logging/settings.py. Goto line number **57**. Replace ***from .cursor_wrapper import CursorLogWrapper*** with ***from django_logging.cursor_wrapper import CursorLogWrapper***. Save the file and exit.
16) python manage.py makemigration
17) python manage.py migrate
18) for cross verifying migrations, run **python manage.py makemigrations team_app**
19) if the above output shows new model Member, then run **python manage.py migrate team_app**
20) python manage.py runserver 8888. Here 8888 is the port on which django server is running.
21) For API Documentation refer to wiki section.


## Steps to run test cases :-
1) cd team_members/team_management_system
2) python manage.py run_test
