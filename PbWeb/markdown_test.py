import markdown

md = markdown.Markdown(extensions=[
    'abbr', 'tables', 'footnotes', 'toc', 'sane_lists', 'fenced_code', 'details',
    'figures', 'yaml', 'latex'
])

# text = """---
# Title: Hello
# ---

# ??? "Summary"
#     Here's some $a+b>c$content.

# ![caption2](img2.jpg)



# $$
# a_2 < 5
# $$

# """

text = r"""

$$
\begin{aligned}
L &= \frac{1}{2}(\sum_{1}^{n}  \lambda_{i}y_{i}X_{i})(\sum_{1}^{n}  \lambda_{i}y_{i}X_{i}) -  \sum_{1}^{n}  \lambda_{i}y_{i} ((\sum_{1}^{n}  \lambda_{i}y_{i}X_{i})X_{i}+b)+\sum_{1}^{n}  \lambda_{i} \\

&= \sum_{1}^{n}  \lambda_{i} - \frac{1}{2}(\sum_{i=1}^{n} \sum_{j=1}^{n}  \lambda_{i} \lambda_{j}y_{i}y_{j}X_{i}^{T}X_{j}) 
\end{aligned}
\tag{4}
$$
"""

print(md.convert(text))
print(md.Meta)
