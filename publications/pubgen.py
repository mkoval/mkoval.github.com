#!/usr/bin/env python
from __future__ import print_function
import argparse, collections, sys
import pybtex.richtext
from pybtex.database.input import bibtex
from pybtex.plugin import find_plugin
from pybtex.style import FormattedBibliography 
from output import JekyllBackend
from style import JekyllStyle
from time import strptime

def get_category(entry):
    note = entry.fields.get('note', '')

    if entry.type == 'article':
        return 'Journal Papers', note
    elif entry.type in [ 'inproceedings', 'conference' ]:
        if note and note.istartswith('workshop'):
            return 'Workshop Papers', note[9:].lstrip()
        else:
            return 'Conference Papers', note
    elif entry.type == 'techreport':
        return 'Technical Reports', note
    else:
        print('warning: Unknown type of entry "{:s}".'.format(entry.type),
              file=sys.stderr)
        return None, None

def get_date_key(entry):
    month_str = entry.fields.get('month', 'January')
    month_index = strptime(month_str, '%B')

    year_str = entry.fields.get('year', '0')
    year_index = strptime(year_str, '%Y')

    return (year_index, month_index)

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
CATEGORIES = [ 'Journal Papers', 'Conference Papers', 'Workshop Papers', 'Technical Reports' ]

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

# Sort the entries by date.
entries.sort(key=get_date_key, reverse=True)
formatted_entries = list(style.format_entries(entries))

# Group the entries by category.
categorized_pubs = collections.defaultdict(list)
for entry, formatted_entry in zip(entries, formatted_entries):
    # Add a link to the PDF if it's specified in the 'howpublished' field.
    if 'howpublished' in entry.fields:
        url = entry.fields['howpublished']
        formatted_entry.text.append(pybtex.richtext.Text(' '))
        formatted_entry.text.append(pybtex.richtext.HRef(url, 'PDF'))

    category, note = get_category(entry)
    entry.fields['note'] = note
    categorized_pubs[category].append(formatted_entry)

output_stream.write(PROLOGUE)

for category_name in CATEGORIES:
    category_entries = categorized_pubs[category_name]

    if category_entries:
        output_stream.write('<h2>{:s}</h2>'.format(category_name))
        category_bib = FormattedBibliography(category_entries, style)
        backend.write_to_stream(category_bib, output_stream)

output_stream.write(EPILOGUE)
