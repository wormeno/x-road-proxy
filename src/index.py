import asyncio
import tornado.ioloop
import tornado.web
import logging
import tornado.options
from SoapConsumer import SoapConsumer


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!")

    def post(self, url):
        print("\r\n")
        print("Iniciando solicitud!!")
        result = SoapConsumer().process_request(self.request)

        self.set_header('Content-Type', 'text/xml')
        logging.info("Process request Ok!")
        self.write(str(result))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/(.*)", MainHandler),
    ], autoreload=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting up')
    app = make_app()
    app.listen(8082)
    tornado.options.parse_command_line
    tornado.ioloop.IOLoop.current().start()
