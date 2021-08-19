import tornado.ioloop
import tornado.web
import tornado.autoreload

from fileio import FileIO

io = FileIO()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = ''
        html += '\n'.join( [ '<li><a href=\"view?id={id}\">{filename}</a></li>'.format(**item) for item in io.get_list() ] )
        self.write(html)


class ViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        file_id = int(self.get_query_argument("id", strip=True))
        html = '<link rel="stylesheet" href="https://typo.sofi.sh/typo.css"/>\n'
        html += io.get_file(file_id)
        self.write(html)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/view", ViewHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(9819)
    tornado.ioloop.IOLoop.current().start()
    # app.stop()
