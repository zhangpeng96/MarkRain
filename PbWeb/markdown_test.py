import markdown

md = markdown.Markdown(extensions=[
    'abbr', 'tables', 'footnotes', 'toc', 'sane_lists', 'fenced_code', 'details',
    'figures', 'yaml'
])

text = """---
Title: Hello
---

??? "Summary"
    Here's some content.

![caption2](img2.jpg)

"""

print(md.convert(text))
print(md.Meta)
