#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 09:07:06 2021

@author: wells
"""

import random
import pandas as pd
from util.util import Util
from categories.category import Category
from global_account.global_account import GlobalAccount
import matplotlib.pyplot as plt
from report.pdfreport import PdfReport



REPORT_FILE = "report/generated_documents/analyse_report.txt"
MONTH_DICT = {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Aout", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}

CAT_SALARY = "Revenus du travail"
CAT_PRROPERTY_INCOME = "Revenus Foncier"
CAT_SOCIAL_SECURITY = "Allocations et Sécurité sociale"

util = Util()
reportFile = open(REPORT_FILE, "w")
pdf = PdfReport(unit='mm')

# Lire le fichier csv dans un dataframe
compte_dataframe = pd.read_csv("DATA/compte.csv", sep=";")
# Remplacement des valeurs NaN dans le dataframe
compte_dataframe = util.replaceNaNValues(compte_dataframe,"Unknown")

list_months = util.getListMonths(compte_dataframe)
list_all_categories = util.getListCategories(compte_dataframe)

list_categories = []


# Suppression des catégories inutiles
categories_to_delete = (CAT_SALARY.lower(),CAT_PRROPERTY_INCOME.lower(),CAT_SOCIAL_SECURITY.lower())
for cat in list_all_categories:
    if cat.lower() not in categories_to_delete:
        list_categories.append(cat)
    
list_months_label = []
for month in list_months:
    list_months_label.append(MONTH_DICT[month])

global_account = GlobalAccount(compte_dataframe)

print("Start analysis...")
print("")
print("1 - create report in txt file")
global_account.createReport(reportFile,"report/generated_documents/")
fig = plt.subplots(figsize=(15, 10))
list_salaries_and_swile = global_account.getListSalariesAndSwile()
list_spent = global_account.getListTotalSpentForMonth("Compte chèques")
plt.plot(list_months_label,list_salaries_and_swile,label="salaires + swile")
plt.plot(list_months_label,list_spent, label="dépenses globales")

for cat in list_categories:
    fig = plt.subplots(figsize=(10, 10))
    category = Category(compte_dataframe,cat)
    list_amount_category = category.getListTotalAmountForMonths()
    category.createReport(reportFile,"report/generated_documents/")
    label_str = "dépense " + cat.lower()
    plt.plot(list_months_label,list_amount_category,label=label_str)
    

plt.xlabel("Mois")
plt.ylabel("Montant en €")
plt.title("Comparaison des dépenses et des salaires")
lg = plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.savefig("report/generated_documents/spent_comparison.png", 
            dpi=150, 
            format='png', 
            bbox_extra_artists=(lg,), 
            bbox_inches='tight')


reportFile.close()
print("create report in txt file ended")

# PDF
print("")
print("2 -create report in pdf file")
pdf.add_page()
pdf.drawFrame()
pdf.addTitle("Rapport de l'analyse des comptes pour l'année 2021".upper(),125, 125, 125)

global_account.createReportInPdf(pdf,"report/generated_documents/")

for cat in list_categories:
    category = Category(compte_dataframe,cat)
    list_amount_category = category.getListTotalAmountForMonths()
    category.createReportInPdf(pdf,"report/generated_documents/")

text = "GRAPHIQUE GENERAL DE COMPARAISON DES DEPENSES"
red_value = random.randint(0, 255)
green_value = random.randint(0, 255)
blue_value = random.randint(0, 255)
pdf.addTitle(text,red_value,green_value,blue_value)
pdf.addPicture("report/generated_documents/spent_comparison.png",720/4,720/5)

pdf.output('analyse_report.pdf','F')
print("create report in pdf file ended")

print("")
print("End analysis.")
 

