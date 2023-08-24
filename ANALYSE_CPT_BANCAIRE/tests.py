#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 08:54:35 2021

@author: wells

Tests
"""

import pandas as pd
from global_account.global_account import GlobalAccount
from util.util import Util
from pandas import DataFrame

util = Util()
reportTestsFile = open("test/test.txt", "w")

# Lire le fichier csv dans un dataframe
account_dataframe = pd.read_csv("DATA/compte.csv", sep=";")
# Remplacement des valeurs NaN dans le dataframe
account_dataframe = util.replaceNaNValues(account_dataframe,"Unknown")

global_account = GlobalAccount(account_dataframe)
global_account_dataframe = global_account.getDataFrame()
df_str = DataFrame.to_string(global_account_dataframe)
reportTestsFile.write(df_str)

print("")

total_salaries = global_account.getTotalSalaryForYear()
print("Total des salaires pour 2021: " + str(total_salaries)+"\n")
list_salaries = global_account.getListSalaries()
print("Liste des salaires: ")
print(list_salaries)
print("")
feb_march_salaries = list_salaries[0] + list_salaries[1]
print("Salaires Février et Mars: " + str(feb_march_salaries) + " €" + "\n")

total_spent_main_account = global_account.getTotalSpent("Compte chèques")
print("Total des dépenses pour le compte chèques: " + str(total_spent_main_account)+ " €")
total_spen_swile_account = global_account.getTotalSpent("Compte Swile")
print("Total des dépenses pour le compte Swile: " + str(total_spen_swile_account)+ " €"+"\n")


total_spent_february = global_account.getTotalSpent("Compte chèques", 2)
total_spent_march = global_account.getTotalSpent("Compte chèques", 3)
total_spent_april = global_account.getTotalSpent("Compte chèques", 4)
print("Dépenses pour Février: " + str(total_spent_february) + " €")
print("Dépenses pour Mars: " + str(total_spent_march) + " €")
print("Dépenses pour Avril: " + str(total_spent_april) + " €" + "\n")

total_spent_february_march = total_spent_february + total_spent_march
print("Dépenses pour Février et Mars: " + str(total_spent_february_march) + " €" + "\n")

list_spent_for_month = global_account.getListTotalSpentForMonth("Compte chèques")
print("Liste des dépenses totales par mois: ")
print(list_spent_for_month)

print("")
categories_spent_year = global_account.getTotalSpentPerCategory("Compte chèques")
print("Dépenses par gatégories sur l'année: ")
for key, value in categories_spent_year.items():
    print(key + ": " + str(value) + " €")

print("")

print("Dépenses par gatégories pour le mois de Février: ")
category_spent_amount_february = global_account.getTotalSpentPerCategory("Compte chèques", 2)
for key, value in category_spent_amount_february.items():
    print(key + ": " + str(value) + " €")

print("")

print("Dépenses par gatégories pour le mois de Mars: ")
category_spent_amount_march = global_account.getTotalSpentPerCategory("Compte chèques", 3)
for key, value in category_spent_amount_march.items():
    print(key + ": " + str(value) + " €")

print("")

print("Dépenses par gatégories pour le mois de Avril: ")
category_spent_amount_april = global_account.getTotalSpentPerCategory("Compte chèques", 4)
for key, value in category_spent_amount_april.items():
    print(key + ": " + str(value) + " €")

print("")

spent_recipient_year = global_account.getAmountByRecipient("Compte chèques")
print("Dépense par bénéficiaire sur l'année: ")
for key, value in spent_recipient_year.items():
    print(key + ": " + str(value) + " €")

print("")
    
spent_recipient_february = global_account.getAmountByRecipient("Compte chèques", 2)
print("Dépense par bénéficiaire pour Février: ")
for key, value in spent_recipient_february.items():
    print(key + ": " + str(value) + " €")


reportTestsFile.close()