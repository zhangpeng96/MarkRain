import os
import markdown
from bs4 import BeautifulSoup
# from lxml.builder import E

class FileIO():
    def __init__(self, dir=''):
        self.dir =  "E:\\文稿\\学术专栏"
        self.file_meta = {}
        self.file_id_count = 1
        self.markdown = markdown.Markdown(
            extensions=['tables', 'footnotes', 'toc', 'sane_lists', 'fenced_code', 'abbr', 'details', 'figures', 'yaml', 'latex']
        )

    def _file_meta_refresh(self):        
        self.file_meta = {}
        self.file_id_count = 1

    def _recur_file(self, path):
        for item in os.listdir(path):
            sub_file = os.path.join(path + "\\" + item)
            if os.path.isdir(sub_file):
                self._recur_file(sub_file)
            else:
                if os.path.splitext(sub_file)[1] == ".md":
                    self.file_meta[self.file_id_count] = {
                        'path': sub_file,
                        'id': self.file_id_count,
                        'rel': os.path.relpath(sub_file, self.dir),
                        'filename': os.path.splitext(os.path.basename(sub_file))[0]
                    }
                    self.file_id_count += 1

    def get_list(self):
        self._file_meta_refresh()
        self._recur_file(self.dir)
        return self.file_meta.values()

    def get_file(self, file_id):
        meta = self.file_meta[file_id]
        with open(meta['path'], 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        html = self.markdown.convert(markdown_text)
        """ 方案一 以yamlmeta为标准
        if self.markdown.Meta:
            if not self.markdown.Meta['title']:
                self.markdown.Meta['title'] = meta['filename']
        else:
            self.markdown.Meta = {}
            self.markdown.Meta['title'] = meta['filename']
        html = '<h1>{}</h1>\n'.format(self.markdown.Meta['title']) + html
        """

        if self.markdown.Meta:
            if self.markdown.Meta.get('title'):
                self.file_meta[file_id]['title'] = self.markdown.Meta['title']
            else:
                self.file_meta[file_id]['title'] = self.file_meta[file_id]['filename']
        else:
            self.file_meta[file_id]['title'] = self.file_meta[file_id]['filename']
        html = '<h1>{}</h1>\n'.format(self.file_meta[file_id]['title']) + html
        # html = etree.tostring(etree.HTML(html), pretty_print=True).decode('utf-8')
        # html = etree.tostring(E.html(etree.fromstring(html))).decode('utf-8')
        # print(elem)
        # html = ''
        # html = BeautifulSoup(html, "html.parser")
        # return html.prettify()
        return html


if __name__ == '__main__':
    io = FileIO()
    print(io.get_list())
