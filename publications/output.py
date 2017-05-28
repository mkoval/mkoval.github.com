# Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011, 2012  Andrey Golovizin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from xml.sax.saxutils import escape
from pybtex.backends import BaseBackend

file_extension = 'html'

class JekyllBackend(BaseBackend):
    name = 'html'
    suffixes = '.html',

    symbols = {
        'ndash': u'&ndash;',
        'newblock': u'\n',
        'nbsp': u'&nbsp;'
    }
    tags = {
         'em': u'em',
         'emph': u'em',
    }
    
    def format_text(self, text):
        return escape(text)

    def format_tag(self, tag_name, text):
        tag = self.tags[tag_name]
        return ur'<%s>%s</%s>' % (tag, text, tag)
    
    def format_href(self, url, text):
        if text == 'PDF':
            class_name = 'pdf'
        elif text.startswith('doi:'):
            class_name = 'doi'
        else:
            class_name = None

        if class_name is not None:
            return ur'<a href="%s" class="%s">%s</a>' % (url, class_name, text)
        else:
            return ur'<a href="%s">%s</a>' % (url, text)

    def write_prologue(self):
        self.output(u'<ul>\n')

    def write_epilogue(self):
        self.output(u'</ul>\n')

    def write_entry(self, key, label, text):
        self.output('<li>%s</li>\n' % text)
