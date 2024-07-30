**AnonLLM - anonymous django AI chat application**

**Instalation**
To install this project to your own machine you should run all commands below.

First of all clone this repository to your computer:
```bash
mkdir anonllm
cd anonllm
git clone https://github.com/vitaliypopel/AnonLLM/
cd AnonLLM
```

Then create vitrual environment:
```bash
python3 -m venv venv
source venv/bin/activate
cd project
python3 -m pip install -r requirements.txt
```

Create .env file with your API_KEY, BASE_URL and MODEL:
```bash
touch .env
nano .env # set your environment
```

After that you can run migrations and run the server:
```bash
python3 manage.py migrate
gunicorn project.wsgi:application
```

Go to browser and open 127.0.0.1:8000/ and..
*Congrats with successfull running! ;D*
