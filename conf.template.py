import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REFRESH_INTERVAL = 1000
HOSTS = ('localhost:9000',)
PORT = 9000

XHEADERS = True

app_settings = {
    "debug": DEBUG,
    "xheaders": XHEADERS
}
