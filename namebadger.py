#!/usr/bin/env python3

from copy import copy
import csv, io, os, re
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import A3, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

CSV_FILE = 'devopsdays-cape-town-2018_guestlist.csv'
FIRSTNAME_COLUMN = 30
LASTNAME_COLUMN = 31

PDF_TEMPLATE = 'A3-Layout-Attendee-Test.pdf'
PDF_SIZE = A3
#PDF_SIZE = A4


a3_positions_2017 = [
    [[106, 1026], [406, 1026]],
    [[106, 725], [406, 725]],
    [[106, 422], [406, 422]],
]

a3_positions_2018 = [
    [[112, 1026], [430, 1026]],
    [[112, 714], [430, 714]],
    [[112, 400], [430, 400]],
]

a4_positions = [
    [[130, 410], [430, 410]],
]

POSITIONS = a3_positions_2018

#TEXT_RGB = (6, 60, 91) # blue
TEXT_RGB = (16, 95, 89) # green

TEXT_START_SIZE = 24

TEXT_SIZE_THRESHOLDS = (
    (220, 16),
    (210, 17),
    (195, 18),
    (180, 19),
    (170, 20),
    (160, 21),
    (150, 22),
    (140, 23),
)

FIRSTNAME_FONT = 'Avenir-Bold'
LASTNAME_FONT = 'Avenir'

pdf_source = open(PDF_TEMPLATE, 'rb')
pdf_in = PdfFileReader(pdf_source)

def determine_size(thing, base_size):
    thing_len = pdfmetrics.stringWidth(thing, 'Avenir', 24)
    print("{} = {}".format(thing, thing_len))
    for threshold in TEXT_SIZE_THRESHOLDS:
        if thing_len > threshold[0] and base_size > threshold[1]:
            return threshold[1]
    return base_size


def names_page(names, positions):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=PDF_SIZE)

    fonts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
    pdfmetrics.registerFont(TTFont("Avenir", os.path.join(fonts_dir, 'avenir.ttf')))
    pdfmetrics.registerFont(TTFont("Avenir-Bold", os.path.join(fonts_dir, 'avenir_bold.ttf')))

    can.setFillColorRGB(TEXT_RGB[0]/256, TEXT_RGB[1]/256, TEXT_RGB[2]/256)

    for index, name in enumerate(names):
        for c in range(0,2):
            x = positions[index][c][0]
            y = positions[index][c][1]
            can.setFont(FIRSTNAME_FONT, determine_size(name[0], TEXT_START_SIZE))
            can.drawString(x, y, name[0].upper())
            can.setFont(LASTNAME_FONT, determine_size(name[1], TEXT_START_SIZE))
            can.drawString(x, y-26, name[1].upper())

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
            last_name = row[LASTNAME_COLUMN].strip()
            #first_name = re.sub('{}$'.format(re.escape(last_name)), '', row[25].strip(), flags=re.IGNORECASE)
            first_name = row[FIRSTNAME_COLUMN].strip()
            attendees.append([first_name, last_name])
    return attendees


output = open('out.pdf', 'wb')
writer = PdfFileWriter()

attendees = load_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), CSV_FILE))
#attendees = attendees[0:12]

#import pprint
#pprint.PrettyPrinter().pprint(attendees)
#import sys
#sys.exit(0)

chunks = [attendees[x:x+len(POSITIONS)] for x in range(0, len(attendees), len(POSITIONS))]
for chunk in chunks:
    packet = names_page(chunk, POSITIONS)
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
