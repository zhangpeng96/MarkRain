import threading
import time
import sys
import random
import webview
# import pymmd
import markdown
from html import unescape


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
caption.source {
  caption-side: bottom;
  font-style: italic;
}
body {margin: 20px;}
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

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grid #2</title>
<style type="text/css">
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: 'Quicksand', sans-serif;
}
.container {
    height: 100vh;
    font-weight: bold;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: 50px 1fr 1fr 50px;
    gap: 2px;
    padding: 10px;
}
.container div {
    padding: 10px;
    border: 1px solid black;
}
.header {
    grid-column-start: 3;
    grid-column-end: 7;
}
.content-large {
    grid-row-start: 1;
    grid-row-end: span 3;
    grid-column: 1/span 2;
}
.content-large {
  font-family: 'SHS Monaco NoAdjust';
  font-size: 11px;
  font-weight: normal;
  overflow: auto;
  line-height: 1.2em;
  white-space: nowrap;
}
.content-large div {
    padding: 0;
    border: none;
}
.content-small {
    grid-row-start: 2;
    grid-row-end: 4;
    grid-column: 3/span 5;
    overflow: auto;
}
.footer {
    grid-column: 1/span 6;
}
</style>
</head>
<body>
  <div class="container">
    <div class="header">Header</div>
    <!-- <div class="content-large" contenteditable="true" id="editor">Navigation</div> -->
    <textarea class="content-large" id="editor">Navigation</textarea>
    <div class="content-small" id="preview"></div>
    <div class="footer">
      <button onClick="getRandomNumber()">TO</button>
    </div>
  </div>
</body>
<script>

    function showResponse(response) {
        var container = document.getElementById('preview')
        container.innerHTML = response.message
        container.style.display = 'block'
    }

    function getRandomNumber() {
        var container = document.getElementById('editor');
        // alert(container.innerText);
        // pywebview.api.getRandomNumber();
        pywebview.api.text(container.value).then(showResponse);
    }
</script>
</html>
"""

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def text(self, md):
        mmd = markdown.Markdown(extensions=['tables', 'footnotes', 'toc', 'sane_lists', 'fenced_code'])
        texts = mmd.convert(md)
        print(texts)
        response = {
            'message': texts
        }
        return response

    def getRandomNumber(self, md):
        response = {
            'message': 'random number: {0} | {}'.format(random.randint(0, 100000000), md)
        }
        print(response)
        return response

def load_html(window):
    time.sleep(5)
    print('ok')



if __name__ == '__main__':
    api = Api()
    window = webview.create_window('MarkRain Editor', html=html, js_api=api, text_select=True)
    # windowhtml=render.get()
    webview.start(load_html, window, debug=True)
