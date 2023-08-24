#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 11:39:41 2021

@author: wells
"""

from report.pdfreport import PdfReport


pdf = PdfReport(unit='mm')
pdf.add_page()
pdf.drawFrame()
pdf.setTitle("Rapport de l'analyse des comptes pour l'année 2021".upper(),220, 50, 50)
pdf.addPicture("report/generated_documents/loisirs_evolution.png",720/6,720/6)
pdf.output('test.pdf','F')
