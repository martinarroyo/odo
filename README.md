# Odo

Odo is a simple server status tool. At its current state it simply retrieves CPU, memory and network stats. It is not very sofisticated, but it does the job for simple monitoring (such as my personal web server).

It uses a websocket connection to the frontend, which is a vanilla JS application written in TypeScript. The stats are retrieved by parsing the output of system commands (`netstat`, `uptime`...), reading `/proc/`, and using a patched version of `sysstat`.

## Installation

### Backend

The backend is a simple Tornado application. Due to the nature of the project, I could not find a proper way to run it on Docker. We'll use a virtual environment instead.

```bash
virtualenv -p python3.6 env
source env/bin/activate
pip install -r requirements.txt

git submodule update --init
cd mpstat
patch -f mpstat.c ../mpstat.patch
./configure && make
cd ..
```

Now edit `conf.template.py` and set your host and port. Disable the debug mode for deployment. Copy it to `conf.py`.

### Frontend

The frontend is compiled with Webpack. Fortunately, here we can use Docker.

```bash
cd frontend
docker-compose build
```

## Running

### Frontend

Simply start the docker container:

```bash
docker-compose up -d
```

### Backend

Simply start `app.py`. A template for [supervisord](http://supervisord.org/) is provided in `deployment/`.

### Proxy

A proxy is required to create a single point of entry for frontend and backend. You can use the nginx template in `deployment/` for reference.
