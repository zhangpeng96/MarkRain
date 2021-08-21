import tornado.ioloop
import tornado.web
import tornado.autoreload
from random import randint
from fileio import FileIO
import os
from lxml import etree

io = FileIO()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = ''
        html += '\n'.join( [ '<li><a href=\"view?id={id}\">{filename}</a></li>'.format(**item) for item in io.get_list() ] )
        self.write(html)


class ViewHandler(tornado.web.RequestHandler):
    def parse_html(self, file_id):
        article = io.get_file(file_id)
        html = """
<html>
<head>
  <title>{}</title>
  <link rel="stylesheet" href="static/han.css?{}"/>
  <link rel="stylesheet" href="https://cdn.mowchan.me/libs/katex/katex.min.css">
</head>
<body>
  <div>
  <p>{}</p>
  </div>
  <div id="write">
    {}
  </div>
  <script src="https://cdn.mowchan.me/libs/katex/katex.min.js"> </script>
  <script src="https://cdn.mowchan.me/libs/katex/auto-render.min.js"> </script>
  <script>
  document.addEventListener("DOMContentLoaded", function() {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "\\\\[", right: "\\\\]", display: true}},
        {{left: "\\\\(", right: "\\\\)", display: true}},
        {{left: "$", right: "$", display: false}}
      ]
    }});
  }});
  </script>
</body>
</html>""".format(io.file_meta[file_id]['title'], randint(1000, 9999),io.file_meta[file_id]['path'], article)
        dom = etree.HTML(html)
        return r'<!DOCTYPE html>' + etree.tostring(dom, pretty_print=True, encoding=str)

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        file_id = int(self.get_query_argument("id", strip=True))
        self.write(self.parse_html(file_id))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/view", ViewHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        static_url_prefix="/static/",
        debug=True
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(9819)
    tornado.ioloop.IOLoop.current().start()
    # app.stop()
