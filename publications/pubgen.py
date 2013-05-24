#!/usr/bin/env python
from __future__ import print_function
import argparse, collections, sys
import pybtex.richtext
from pybtex.database.input import bibtex
from pybtex.plugin import find_plugin
from pybtex.style import FormattedBibliography 
from output import JekyllBackend
from style import JekyllStyle

PROLOGUE = u"""\
---
layout: default
title: Publications - Michael Koval
category: publications 
---
"""
EPILOGUE = u"""\
<div style="font-style:italic;font-size:0.8em;text-align:center;">This page is automatically
generated from a <a href="mkoval.bib">BibTeX file</a> using <a
href="http://pybtex.sourceforge.net/">Pybtex</a>.</div>
"""
CATEGORIES = collections.OrderedDict([
    ('Journal Papers', [ 'article' ]),
    ('Conference Papers', [ 'inproceedings' ]),
    ('Technical Reports', [ 'techreport' ]),
])

arg_parser = argparse.ArgumentParser(description='Generates an HTML publication list from BibTeX.')
arg_parser.add_argument('input_file')
arg_parser.add_argument('--style', default='plain')
args = arg_parser.parse_args()
output_stream = sys.stdout

style_cls = find_plugin('pybtex.style.formatting', args.style)

style = JekyllStyle()
backend = JekyllBackend()

bib_parser = bibtex.Parser()
bib_file = bib_parser.parse_file(args.input_file)
entries = bib_file.entries.values()
formatted_entries = list(style.format_entries(entries))

categorized_pubs = collections.defaultdict(list)
for entry, formatted_entry in zip(entries, formatted_entries):
    # Add a link to the PDF if it's specified in the 'howpublished' field.
    if 'howpublished' in entry.fields:
        url = entry.fields['howpublished']
        formatted_entry.text.append(pybtex.richtext.Text(' '))
        formatted_entry.text.append(pybtex.richtext.HRef(url, 'PDF'))

    categorized_pubs[entry.type].append(formatted_entry)

output_stream.write(PROLOGUE)
for category_name, types in CATEGORIES.items():
    merged_entries = reduce(lambda x, y: x + y, [ categorized_pubs[type] for type in types ], [])

    if merged_entries:
        output_stream.write('<h2>%s</h2>' % category_name)
        category_bib = FormattedBibliography(merged_entries, style)
        backend.write_to_stream(category_bib, output_stream)
output_stream.write(EPILOGUE)
