#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 11:36:28 2021

@author: Jocelynn GIROD
Classe pour la génération du report en pdf
"""

from fpdf import FPDF

class PdfReport(FPDF):
    
    pdf_w = 210
    pdf_h = 297
    
    
    # Définie un titre
    def addTitle(self,title,r_color,g_color,b_color):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(r_color, g_color, b_color)
        self.cell(w=210.0, h=20.0, align='C', txt=title, border=0,ln=1)
        self.ln(10)
    
    # Dessine un cadre gris
    def drawFrame(self):
        self.set_line_width(0.5)
        self.set_fill_color(125.0, 125.0, 125.0)
        self.rect(2.0, 2.0, 206.0,293.0,'DF')
        self.set_fill_color(255, 255, 255)
        self.rect(3.0, 3.0, 204.0,291.0,'FD')
        
    # Ajoute une image
    def addPicture(self,picture_path,width,height):
        self.image(picture_path,  link='', type='PNG', w=width, h=height)
        
    # Ajoute du texte
    def addText(self,text,r_color,g_color,b_color,is_ln=True):
        self.set_font('Arial', '', 10)
        self.set_text_color(r_color, g_color, b_color)
        if is_ln:
            self.cell(w=0.0, h=5.0, align='L', txt=text, border=0,ln=1)
        else:
            self.cell(w=self.get_string_width(text), h=5.0, align='L', txt=text, border=0,ln=0)
    
        
    # Ajoute un titre de chapitre
    def addChapterTitle(self,text,r_color,g_color,b_color):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(r_color, g_color, b_color)
        self.cell(w=0, h=6, txt=text, border=0, ln=1, align='L')
        self.ln(4)
    
    # Ajoute un sous-titre de chapitre
    def addSubTitle(self,text,r_color,g_color,b_color):
        self.set_font('Arial', 'BI', 11)
        self.set_text_color(r_color, g_color, b_color)
        self.cell(w=0, h=6, txt=text, border=0, ln=1, align='L')
        self.ln(2)
        
    