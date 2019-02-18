import json
import sys


from tornado import websocket
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.httpserver import HTTPServer
from tornado.web import Application

import conf
from statuscrawler import get_data

io_loop = IOLoop.instance()


open_ws = set()

data_json = ""

async def process_data():
    global data_json
    data_dict = await get_data()
    data_json = json.dumps(data_dict)

class CallbackHandler():
    callback_fn = None

    def start_callback(self):
        if self.callback_fn is None:
            self.callback_fn = PeriodicCallback(process_data, conf.REFRESH_INTERVAL)
            self.callback_fn.start()
        elif not self.callback_fn.is_running():
            self.callback_fn.start()
    def stop_callback(self):
        callback_fn.stop()


class WebSocketIndexHandler(websocket.WebSocketHandler):
    def check_origin(self, origin): return True
    def open(self):
        open_ws.add(self)
        self.callback = PeriodicCallback(self.send_data, 1000)
        self.callback.start()
    
    def send_data(self):
        self.write_message(data_json)

    def on_close(self):
        self.callback.stop()
        open_ws.remove(self)

routes = [
     (r'/ws/monitor', WebSocketIndexHandler),
]


def main():
    app = Application(routes, **conf.app_settings)

    callback_handler = CallbackHandler()
    callback_handler.start_callback()


    http_server = HTTPServer(app)

    http_server.listen(conf.PORT)

    io_loop.start()

if __name__ == "__main__":
    sys.exit(main())

