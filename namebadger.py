#!/usr/bin/env python3

from copy import copy
import csv
import io
import os
import re
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdf_source = open('badges-a3.pdf', 'rb')
pdf_in = PdfFileReader(pdf_source)


def determine_size(thing, base_size):
    thing_len = pdfmetrics.stringWidth(thing, 'Avenir', 24)
    print("{} = {}".format(thing, thing_len))
    thresholds = (
        (220, 16),
        (210, 17),
        (195, 18),
        (180, 19),
        (170, 20),
        (160, 21),
        (150, 22),
        (140, 23),
    )
    for threshold in thresholds:
        if thing_len > threshold[0] and base_size > threshold[1]:
            return threshold[1]
    return base_size


def names_page(names):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A3)

    fonts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
    pdfmetrics.registerFont(TTFont("Avenir", os.path.join(fonts_dir, 'avenir.ttf')))
    pdfmetrics.registerFont(TTFont("Avenir-Bold", os.path.join(fonts_dir, 'avenir_bold.ttf')))

    can.setFillColorRGB(6/256, 60/256, 91/256)

    positions = [
        [110, 1056],
        [425, 1056],
        [110, 740],
        [425, 740],
        [110, 424],
        [425, 424],
    ]

    for index, name in enumerate(names):
        x = positions[index][0]
        y = positions[index][1]
        can.setFont('Avenir-Bold', determine_size(name[0], 24))
        can.drawString(x, y, name[0].upper())
        can.setFont('Avenir', determine_size(name[1], 24))
        can.drawString(x, y-26, name[1].upper())
        #can.setFont('Avenir', determine_size(name[2], 20))
        #can.drawString(x, y-26-32, name[2])

    can.showPage()
    can.save()
    packet.seek(0)
    return packet


def load_csv(path):
    attendees = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            last_name = row[26].strip()
            first_name = re.sub('{}$'.format(re.escape(last_name)), '', row[25].strip(), flags=re.IGNORECASE)
            attendees.append([first_name, last_name])
    return attendees


output = open('out.pdf', 'wb')
writer = PdfFileWriter()

attendees = load_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'devopsdays-cape-town-2016_guestlist.csv'))
#import pprint
#pprint.PrettyPrinter().pprint(attendees)
#import sys
#sys.exit(0)
chunks = [attendees[x:x+6] for x in range(0, len(attendees), 6)]
for chunk in chunks:
    packet = names_page(chunk)
    pdf_new = PdfFileReader(packet)
    page = copy(pdf_in.getPage(0))
    page.mergePage(pdf_new.getPage(0))
    writer.addPage(page)

blank = copy(pdf_in.getPage(0))
writer.addPage(blank)

writer.write(output)
output.close()

#for i in range(0, 5):
#    writer.appendPagesFromReader(pdf_in)
