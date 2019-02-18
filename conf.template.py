import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(BASE_DIR, 'build')

REFRESH_INTERVAL = 1000
PORT = 9000

XHEADERS = True

app_settings = {
    "debug": DEBUG,
    "static_path": STATIC_PATH,
    "xheaders": XHEADERS
}
