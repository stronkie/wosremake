#!/usr/bin/env python3
"""walkthrough.txt -> print/WorldOfStronkieII_Walkthrough.pdf (A4, Courier)"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lines = open(os.path.join(HERE, 'walkthrough.txt')).read().splitlines()
out = os.path.join(HERE, 'print', 'WorldOfStronkieII_Walkthrough.pdf')
c = canvas.Canvas(out, pagesize=A4)
c.setTitle('The World of Stronkie II - Walkthrough')
c.setAuthor('Mark Stronks, Stronkie Soft')
W, H = A4
size, lead, top, left = 8.6, 10.4, H - 40, 40
y = top
page = 1
for ln in lines:
    if y < 50:
        c.setFont('Courier', 7)
        c.drawCentredString(W / 2, 25, f'- {page} -')
        c.showPage()
        page += 1
        y = top
    c.setFont('Courier', size)
    c.drawString(left, y, ln)
    y -= lead
c.setFont('Courier', 7)
c.drawCentredString(W / 2, 25, f'- {page} -')
c.save()
print(out, page, 'pages')
