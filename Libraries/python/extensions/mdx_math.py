# -*- coding: utf-8 -*-

'''
Math extension for Python-Markdown
==================================

Adds support for displaying math formulas using
[MathJax](http://www.mathjax.org/).

Author: 2015-2020, Dmitry Shachnev <mitya57@gmail.com>.
'''

from xml.etree.ElementTree import Element
from ..inlinepatterns import InlineProcessor
from . import Extension
from html import unescape
from ..postprocessors import Postprocessor
# from ..preprocessors import Preprocessor
from ..util import AtomicString


# def _wrap_node(node, preview_text, wrapper_tag):
#     preview = Element('span', {'class': 'MathJax_Preview'})
#     preview.text = AtomicString(preview_text)
#     wrapper = Element(wrapper_tag)
#     wrapper.extend([preview, node])
#     return wrapper


class InlineMathPattern(InlineProcessor):
    def handleMatch(self, m, data):
        node = Element('escape')
        node.text = AtomicString(' ${}$ '.format(m.group(2)))
        return node, m.start(0), m.end(0)
        # text = ' ${}$ '.format(m.group(2))
        # text = AtomicString(' ${}$ '.format(m.group(2)))
        # node = Element('script')
        # node.set('type', self._content_type)
        # node.text = AtomicString(m.group(2))
        # if self._add_preview:
        #     node = _wrap_node(node, m.group(0), 'span')
        # return node, m.start(0), m.end(0)
        # print(m.match(), data, m.groups())
        # return text, m.start(0), m.end(0)


class DisplayMathPattern(InlineProcessor):
    def handleMatch(self, m, data):
        print('*************')
        node = Element('escape')
        node.text = AtomicString('\n$$\n{}\n$$\n'.format(m.group(2).strip('\n')))
        return node, m.start(0), m.end(0)
        # text = '$$\n{}\n$$'.format(AtomicString(m.group(2).strip('\n')))
        # text = AtomicString('$$\n{}\n$$'.format(m.group(2).strip('\n')))
        # node = Element('script')
        # node.set('type', '%s; mode=display' % self._content_type)
        # if '\\begin' in m.group(1):
        #     node.text = AtomicString(m.group(0))
        # else:
        #     node.text = AtomicString(m.group(2))
        # if self._add_preview:
        #     node = _wrap_node(node, m.group(0), 'div')
        # return node, m.start(0), m.end(0)
        # print(m.groups())
        # return text, m.start(0), m.end(0)


# class ShowLaTeXPostprocesor(Postprocessor):
#     def run(self, text):
#         print('>>>', len(text), text)
#         # text = text.replace('<p>'
#         return unescape(text)

class MathExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'enable_dollar_delimiter':
                [True, 'Enable single-dollar delimiter']
        }
        super(MathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        inlinemathpatterns = (
            InlineMathPattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),    #  $...$
            InlineMathPattern(r'(?<!\\)(\\\()(.+?)(\\\))')       # \(...\)
        )
        mathpatterns = (
            DisplayMathPattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'),  # $$...$$
            DisplayMathPattern(r'(?<!\\)(\\\[)(.+?)(\\\])'),     # \[...\]
            DisplayMathPattern(                            # \begin...\end
                r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\2})')
        )
        if not self.getConfig('enable_dollar_delimiter'):
            inlinemathpatterns = inlinemathpatterns[1:]

        for i, pattern in enumerate(mathpatterns):
            # we should have higher priority than 'escape' which has 180
            # print(pattern)
            md.inlinePatterns.register(pattern, 'math-%d' % i, 185)
        for i, pattern in enumerate(inlinemathpatterns):
            # to use gitlab delimiters, we should have higher priority than
            # 'backtick' which has 190
            # priority = 195 if use_gitlab_delimiters else 185
            md.inlinePatterns.register(pattern, 'math-inline-%d' % i, 185)
        if self.getConfig('enable_dollar_delimiter'):
            md.ESCAPED_CHARS.append('$')
        # md.postprocessors.register(ShowLaTeXPostprocesor(md), 'latex_raw', 181)


def makeExtension(*args, **kwargs):
    return MathExtension(*args, **kwargs)
