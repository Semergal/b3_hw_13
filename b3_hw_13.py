class HTML:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Собираем все части и окончательно форматируем
        html_start = "<html>\n"
        html_end = "\n</html>"
        head_title = '<%s>' % head + str(title) + '</%s>\n' % head
        body_start = '<%s>' % body
        body_end = '\n</%s>' % body
        h1_in_body = str(h1)
        div_start = '\t<%s>' % div
        div_end = '\n\t</%.*s>' % (3, div)
        p = '%s' % paragraph
        img_in_div = '\t<%s>' % img
        # Записываем результат в файл
        f = open('index.html', 'w')
        f.write(html_start + head_title + body_start + h1_in_body + div_start +
              p.expandtabs(8) + img_in_div.expandtabs(8) + div_end + body_end +
              html_end)
        f.close()


class TopLevelTag:
    # Теги без классов
    def __init__(self, tag):
        self.tag = tag

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def __str__(self):
        if self.tag == 'head':
            return '{0}'.format(self.tag)
        if self.tag == 'body':
            return '{0}'.format(self.tag)


class Tag:
    def __init__(self, tag, klass=None, id=None, data_image=None):
        self.tag = tag
        self.text = ''
        self.attrs = {}
        self.args = []
        self.src = ''
        self.data = []

        if klass is not None:
            self.attrs['class'] = ' '.join(klass)
        if id is not None:
            self.args.append(id)
        if data_image is not None:
            self.data.append(data_image)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def __str__(self):
        # Title
        if self.tag == 'title':
            return '\n\t<{0}>{1}</{0}>\n'.format(self.tag, self.text)
        # H1
        if self.tag == 'h1':
            class_attrs = []
            for v in self.attrs.values():
                class_attrs.append(v)
            class_in_tag: str = 'class="{0}"'.format(*class_attrs)
            return '\n\t<{0} {2}>{1}</{0}>\n'.format(self.tag, self.text,
                                                     class_in_tag)
        # Div
        if self.tag == 'div':
            tag = '{0}'.format(self.tag)
            class_attrs = []
            for v in self.attrs.values():
                class_attrs.append(v)
            class_in_tag: str = 'class="{0}"'.format(*class_attrs)
            id_in_tag: str = 'id="{0}"'.format(*self.args)
            return tag + ' ' + class_in_tag + ' ' + id_in_tag
        # P
        if self.tag == 'p':
            return '\n\t<{0}>{1}</{0}>\n'.format(self.tag, self.text)
        # IMG
        if self.tag == 'img':
            tag = '{0} src="{1}"'.format(self.tag, self.src)
            data_image_in_tag: str = ' data-image="{0}"/'.format(*self.data)
            return tag + data_image_in_tag


if __name__ == '__main__':
    with HTML() as html:
        with TopLevelTag('head') as head:
            with Tag('title') as title:
                title.text = 'hello'

        with TopLevelTag('body') as body:
            with Tag('h1', klass=('main-text',)) as h1:
                h1.text = 'Test'
            with Tag('div', klass=('container', 'container-fluid'),
                     id='lead') as div:
                with Tag('p') as paragraph:
                    paragraph.text = 'another test'

                with Tag('img', data_image='responsive') as img:
                    img.src = '/icon.png'