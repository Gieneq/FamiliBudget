# FamiliBudget

Budget app to control you income and expenses. Done using Django, Django REST Framework and Docker Compose.

## Instalation Linux

Install Docker and Docker Compose:

```commandline
sudo apt-get install docker 
sudo apt-get install docker-compose-plugin
```

Download repo using Git and move inside downloaded folder:

```commandline
git clone https://github.com/Gieneq/FamiliBudget.git
cd FamiliBudget/
```

Run Docker Copmpose:
```commandline
docker-compose up --build
```

After completion check running containers:
```commandline
sudo docker ps
```
It will look like this:
```
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                                       NAMES
125a62cfa4b1   family_budget_web   "bash -c 'python man…"   36 seconds ago   Up 35 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   family_budget_web_1
dd133aebe476   postgres            "docker-entrypoint.s…"   13 hours ago     Up 35 seconds   5432/tcp                                    family_budget_db_1
```
You can check if current location (workdir) is the same as in Dockerfile /code by typing:
```commandline
sudo docker exec -it 12 pwd
```

## Setup data
We will use running container with web app. It's IP changes. You can use only first representative characters of ID.

First migrate models:
```commandline
sudo docker exec -it 12 python manage.py migrate
```

Create superuser:
```commandline
sudo docker exec -it 12 python manage.py createsuperuser
```

Load data fixtures to prefeed database using fixtures.json file. It should be inlcuded to the container. You can check it using ls:
```commandline
sudo docker exec -it 12 ls -lah
```

```text
drwxrwxr-x 10 1000 1000 4.0K Sep 17 12:22 .
drwxr-xr-x  1 root root 4.0K Sep 17 12:00 ..
-rw-rw-r--  1 1000 1000  181 Sep 16 23:36 .dockerignore
-rw-rw-r--  1 1000 1000   82 Sep 16 23:03 .env
drwxrwxr-x  8 1000 1000 4.0K Sep 17 11:17 .git
-rw-rw-r--  1 1000 1000   54 Sep 17 11:10 .gitignore
drwxrwxr-x  3 1000 1000 4.0K Sep 17 12:09 .idea
-rw-rw-r--  1 1000 1000  408 Sep 17 10:41 Dockerfile
-rw-rw-r--  1 1000 1000 1.8K Sep 17 12:22 README.md
drwxrwxr-x  4 1000 1000 4.0K Sep 17 12:07 budget
drwxr-xr-x  3 root root 4.0K Sep 16 22:47 data
-rw-rw-r--  1 1000 1000  508 Sep 17 11:49 docker-compose.yml
drwxr-xr-x  4 1000 1000 4.0K Sep 17 10:31 familybudget
-rw-rw-r--  1 1000 1000 1.4K Sep 17 12:00 fixtures.json
-rwxr-xr-x  1 1000 1000  668 Sep 16 22:47 manage.py
-rw-rw-r--  1 1000 1000   90 Sep 17 10:15 requirements.txt
drwxrwxr-x  4 1000 1000 4.0K Sep 17 10:26 share
drwxrwxr-x  4 1000 1000 4.0K Sep 17 10:24 userprofile
drwxrwxr-x  4 1000 1000 4.0K Sep 17 09:27 venv

```

```commandline
sudo docker exec -it 12 python manage.py loaddata fixtures.json
```