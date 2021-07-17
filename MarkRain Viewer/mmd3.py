import threading
import time
import sys
import random
import webview
# import pymmd
import markdown

style_start = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
table {
    border-collapse: collapse;
}
table td, colgroup, tr, th, tbody, thead{
    border: 1px solid #aaa;
    padding: 5px;
}
"""

style_end = """
body {margin: 20px;}
caption.source {
  caption-side: bottom;
  font-style: italic;
}
</style>
</head>
<body>
<div>
<button onClick="getRandomNumber()">open file</button><br/>
</div>
"""


html_foot = """
<script>
    function getRandomNumber() {
        pywebview.api.getRandomNumber()
    }
</script>
</body>
</html>
"""

class HtmlRender:
    def __init__(self, window):
        self.path = ''
        self.html = ''
        self.window = window

    def get(self):
        return self.html

    def process(self):
        md = markdown.Markdown(extensions=['tables', 'footnotes', 'toc', 'sane_lists', 'fenced_code'])
        with open(self.path, "r", encoding="utf-8") as f:
            text = f.read()
        with open('style.css', 'r', encoding='utf-8') as f:
            style = f.read()
        self.html = style_start + style + style_end + md.convert('[TOC]\n\n' + text) + html_foot
        print(time.time())
        self.window.load_html(self.html)
        window.set_title('File: {}'.format(self.path))
        self.window.loaded += on_loaded

    def open_file(self, window):
        file_types = ('Markdown (*.md;*.mmd;*.markdown)', 'All files (*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        self.path = result[0]
        self.process()

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def getRandomNumber(self, window):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(random.randint(0, 100000000))
        }
        print(response)
        return response



def on_loaded():
    print('DOM is ready')
    # unsubscribe event listener
    # 
    print(on_loaded)
    print(time.time())
    webview.windows[0].loaded -= on_loaded
# def open_file(window):
#     # file_types = ('Markdown (*.md;*.mmd;*.markdown)', 'All files (*.*)')
#     file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
#     result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
#     print(result[0])

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('MultiMarkdown', html="<html></html>", js_api=api, text_select=True)
    render = HtmlRender(window)
    # windowhtml=render.get()
    webview.start(render.open_file, window, debug=True)
    # webview.start(open_file, window)
