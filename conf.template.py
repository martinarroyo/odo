import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REFRESH_INTERVAL = 1000
HOSTS = ('localhost:8009',)
PORT = 8009

XHEADERS = True

app_settings = {
    "debug": DEBUG,
    "xheaders": XHEADERS
}
