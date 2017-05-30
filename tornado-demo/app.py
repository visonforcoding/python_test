import tornado.ioloop
import tornado.web
from config import Env,route
import os

def make_app():
    return tornado.web.Application(
        handlers = route.handler,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(Env.SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()
