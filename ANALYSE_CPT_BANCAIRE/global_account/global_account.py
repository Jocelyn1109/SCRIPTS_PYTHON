#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:17:33 2021

@author: wells

Classe pour les comptes et les dépenses globales
"""

import pandas as pd
from pandas import Series
from pandas import DataFrame
from util.util import Util

CATEGORY_COLUMN = "category"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"
MONTH_COLUMN = "month"
ACCOUNT_COLUMN = "account"
MODE_COLUMN = "mode"
RECIPIENT_COLUMN = "payee"

TRANSFERT_MODE = "Transfert bancaire"
CATEGORY_NET_SALARY = "Revenus du travail > Salaire net"
MAIN_ACCOUNT = "Compte chèques"
SWILE_ACCOUNT = "Compte Swile"
MONTH_DICT = {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Aout", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}
BLACK_RGB = (0,0,0)
RED_RGB = (236,34,34)
GREEN_RGB = (9,93,5)
BLUE_TITLE_RGB = (14,65,215)
BLUE_SUBTITLE_RGB = (86,118,212)
TAB = "  - "


class GlobalAccount:
    util = Util()
    global_account_dataframe = None
    months_labels = []
    month_list = []

    def __init__(self, dataframe):
        if self.util.checkDataFrame(dataframe):
            self.global_account_dataframe = dataframe
            # Conversion de la colonne date en datetime
            self.global_account_dataframe[DATE_COLUMN] = pd.to_datetime(self.global_account_dataframe[DATE_COLUMN])
            # Ajout de la colonne month
            self.global_account_dataframe[MONTH_COLUMN] = self.global_account_dataframe[DATE_COLUMN].dt.month
            # Suppression des colonnes inutiles
            self.global_account_dataframe = self.util.dropUselessColumns(self.global_account_dataframe)

            months = self.global_account_dataframe[MONTH_COLUMN].unique()
            for m in months:
                self.months_labels.append(MONTH_DICT[m])

            self.month_list = self.global_account_dataframe[MONTH_COLUMN].unique()


    # Récupère le dataframe
    def getDataFrame(self):
        return self.global_account_dataframe

    # Récupère les montant total des salaires sur l'année
    def getTotalSalaryForYear(self):
        if self.util.checkDataFrame(self.global_account_dataframe):
            tmp_dataframe = self.global_account_dataframe[self.global_account_dataframe[CATEGORY_COLUMN] == CATEGORY_NET_SALARY]
            return tmp_dataframe[AMOUNT_COLUMN].sum()
        else:
            return 0

    # Récupère la liste des salaires
    def getListSalaries(self):
        list_salaries = []
        for month in self.month_list:
            row = self.global_account_dataframe[(self.global_account_dataframe[CATEGORY_COLUMN] == CATEGORY_NET_SALARY) & (self.global_account_dataframe[MONTH_COLUMN] == month)]
            salary = row.iloc[0][AMOUNT_COLUMN]
            list_salaries.append(salary)

        return list_salaries


    # Récupère la liste des salaires ajoutés des rentrés du comptes Swile
    def getListSalariesAndSwile(self):
        list_salaries_and_swile = []
        for month in self.month_list:
             # Récupération des valeurs positives qui correpondent à une rentrée d'argent
            tmp_dataframe = self.global_account_dataframe[self.global_account_dataframe[AMOUNT_COLUMN] > 0]
            # On récupère les salaires et les tickets restaurant
            salary = tmp_dataframe[(tmp_dataframe[CATEGORY_COLUMN] == CATEGORY_NET_SALARY) & (tmp_dataframe[MONTH_COLUMN] == month)].iloc[0][AMOUNT_COLUMN]

            tmp_dataframe = tmp_dataframe[(tmp_dataframe[ACCOUNT_COLUMN] == SWILE_ACCOUNT) & (tmp_dataframe[MONTH_COLUMN] == month)]

            if not tmp_dataframe[(tmp_dataframe[ACCOUNT_COLUMN] == SWILE_ACCOUNT) & (tmp_dataframe[MONTH_COLUMN] == month)].empty:
                swile =  tmp_dataframe[(tmp_dataframe[ACCOUNT_COLUMN] == SWILE_ACCOUNT) & (tmp_dataframe[MONTH_COLUMN] == month)].iloc[0][AMOUNT_COLUMN]
            else:
                swile = 0

            total = round((salary + swile),2)
            list_salaries_and_swile.append(total)

        return list_salaries_and_swile


    # Récupère le total des dépenses pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalSpent(self,account,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")

        if self.util.checkDataFrame(self.global_account_dataframe):
            tmp_dataframe = self.global_account_dataframe.copy()

            filePath = ""
            # Récupération des valeurs négatives qui correpondent à une dépense
            if month > 0:
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account) & (tmp_dataframe[MONTH_COLUMN] == month) & (tmp_dataframe[MODE_COLUMN] != TRANSFERT_MODE)]
                filePath = "test/spent_for_month_ " + str(month) + ".txt"
            else:
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account) & (tmp_dataframe[MODE_COLUMN] != TRANSFERT_MODE)]
                filePath = "test/spent_for_year.txt"


            # Suppression des -
            tmp_dataframe[AMOUNT_COLUMN] = tmp_dataframe[AMOUNT_COLUMN] * (-1)

            # Only for debug _ comment otherwise
            file = open(filePath, "w")
            df_str = DataFrame.to_string(tmp_dataframe)
            file.write(df_str)
            file.close()

            return round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
        else:
            return 0


    # Récupère la liste des dépenses par mois
    def getListTotalSpentForMonth(self,account):
        list_spent = []
        if self.util.checkDataFrame(self.global_account_dataframe):
            for month in self.month_list:
                tmp_dataframe = self.global_account_dataframe.copy()
                # Récupération des valeurs négatives qui correpondent à une dépense
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account) & (tmp_dataframe[MONTH_COLUMN] == month) & (tmp_dataframe[MODE_COLUMN] != TRANSFERT_MODE)]
                # Suppression des -
                tmp_dataframe[AMOUNT_COLUMN] = tmp_dataframe[AMOUNT_COLUMN] * (-1)
                spent = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                list_spent.append(spent)

        return list_spent


    # Récupère le total des dépenses par catégorie pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalSpentPerCategory(self,account, month=0):
        categories_amount = dict()

        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")

        if self.util.checkDataFrame(self.global_account_dataframe):
            tmp_dataframe = self.global_account_dataframe.copy()

            # Récupération des valeurs négatives qui correpondent à une dépense avec filtres (compte, mois,...)
            filePath = ""
            if month > 0:
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account) & (tmp_dataframe[MONTH_COLUMN] == month) & (tmp_dataframe[MODE_COLUMN] != TRANSFERT_MODE)]
                filePath = "test/spent_per_category_month_" + str(month) + ".txt"
            else:
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account) & (tmp_dataframe[MODE_COLUMN] != TRANSFERT_MODE)]
                filePath = "test/spent_per_category_year.txt"

            # Suppression des -
            tmp_dataframe[AMOUNT_COLUMN] = tmp_dataframe[AMOUNT_COLUMN] * (-1)

            # Only for debug _ comment otherwise
            file = open(filePath, "w")
            df_str = DataFrame.to_string(tmp_dataframe)
            file.write(df_str)
            file.close()

            cats = tmp_dataframe[CATEGORY_COLUMN].unique()
            cats = sorted(cats)
            for c in cats:
                df = tmp_dataframe[tmp_dataframe[CATEGORY_COLUMN] == c]
                sum_cat = df[AMOUNT_COLUMN].sum()
                categories_amount[c] = round(sum_cat,2)


        return categories_amount


    # Récupère le total des dépenses par bénéficiaire pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getAmountByRecipient(self, account, month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")

        recipient_list = self.global_account_dataframe[RECIPIENT_COLUMN].unique()
        recipient_amount_dict = dict()
        if self.util.checkDataFrame(self.global_account_dataframe):
            tmp_dataframe = self.global_account_dataframe.copy()

            filePath = ""
            # Récupération des valeurs négatives qui correpondent à une dépense
            if month > 0:
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account) & (tmp_dataframe[MONTH_COLUMN] == month)]
                filePath = "test/spent_recipient_month_" + str(month) + ".txt"
            else:
                tmp_dataframe = tmp_dataframe[(tmp_dataframe[AMOUNT_COLUMN] < 0) & (tmp_dataframe[ACCOUNT_COLUMN] == account)]
                filePath = "test/spent_recipient_year.txt"

            # Suppression des -
            tmp_dataframe[AMOUNT_COLUMN] = tmp_dataframe[AMOUNT_COLUMN] * (-1)

            # Only for debug _ comment otherwise
            file = open(filePath, "w")
            df_str = DataFrame.to_string(tmp_dataframe)
            file.write(df_str)
            file.close()

            for rcp in recipient_list:
                df = tmp_dataframe[tmp_dataframe[RECIPIENT_COLUMN] == rcp]
                sum_rcp = df[AMOUNT_COLUMN].sum()
                recipient_amount_dict[rcp] = round(sum_rcp,2)

        return recipient_amount_dict


    # Retourne les statistiques de la colonne amount pour l'année
    def getStatsForYear(self,file):
        if self.util.checkDataFrame(self.global_account_dataframe):
            file.write(Series.to_string(self.global_account_dataframe[AMOUNT_COLUMN].describe())+"\n")

    # Retourne les statistiques de la colonne amount pour le mois
    def getStatsForMonth(self,month,file):
        if self.util.checkDataFrame(self.global_account_dataframe):
            tmp_dataframe = self.global_account_dataframe[self.global_account_dataframe[MONTH_COLUMN] == month]
            file.write(Series.to_string(tmp_dataframe[AMOUNT_COLUMN].describe())+"\n")




    # Imprime le rapport dans un fichier texte
    def createReport(self,file,directory):

        file.write("Rapport de l'analyse globale des comptes pour l'année 2021".upper()+"\n")
        file.write("-----------------------------------------------------------"+"\n"+"\n")
        total_salaries_for_year = self.getTotalSalaryForYear()
        total_spent_for_year = self.getTotalSpent(MAIN_ACCOUNT)
        file.write("- GLOBAL: Somme totale des salaires nets pour l'année: " + str(total_salaries_for_year) + " €"+"\n")
        file.write("- GLOBAL: Somme totale des dépenses sur l'année sur le compte chèque: " + str(total_spent_for_year) + " €"+"\n")
        file.write("- GLOBAL: Delta entre le total des salaires et le total des dépenses: " + str(round(total_salaries_for_year - total_spent_for_year, 2)) + " €"+"\n"+"\n")

        categories_amount = self.getTotalSpentPerCategory(MAIN_ACCOUNT)
        file.write("GLOBAL: Dépenses par catégories sur l'année: "+"\n")
        for key, value in categories_amount.items():
            percentage = round((value * 100) / total_spent_for_year, 2)
            file.write("\t" + key + ": " + str(value) + " € (soit " + str(percentage) + " % des dépenses totales)"+"\n")

        file.write("\n")

        recipient_amount = self.getAmountByRecipient(MAIN_ACCOUNT)
        file.write("GLOBAL: Total des dépenses par bénéficiaire sur l'année: "+"\n")
        for key, value in recipient_amount.items():
            file.write("\t" + key + ": " + str(value) + " €"+"\n")

        file.write("\n")
        month_list_amount = []
        for month in self.month_list:
            month_spent = round(self.getTotalSpent(MAIN_ACCOUNT,month),2)
            month_list_amount.append(month_spent)
            file.write("- GLOBAL: Dépense totale pour le mois de " + MONTH_DICT[month] + ": " + str(month_spent) + " €"+"\n")

        file.write("\n")
        for month in self.month_list:
            file.write("Dépenses par catégories pour le mois de: " + MONTH_DICT[month]+ ":" + "\n")
            categories_amount = self.getTotalSpentPerCategory(MAIN_ACCOUNT, month)
            for key, value in categories_amount.items():
                percentage = round((value * 100) / round(self.getTotalSpent(MAIN_ACCOUNT,month),month), 2)
                file.write("\t" + key + ": " + str(value) + " € (soit " + str(percentage) + " % des dépenses totales)"+"\n")

            file.write("\n")

        file.write("\n")
        
        for month in self.month_list:
            file.write("Total des dépenses par bénéficiaire pour le mois de " + MONTH_DICT[month] + ": " + "\n")
            recipient_amount = self.getAmountByRecipient(MAIN_ACCOUNT,month)
            for key, value in recipient_amount.items():
                file.write("\t" + key + ": " + str(value) + " €")
            
            file.write("\n")

        x_values = self.months_labels
        y_values = month_list_amount
        self.util.createDiagram(x_values, y_values, "Mois", "Montant en €", "Evolution des dépenses globales par mois", True, directory + "spent_evolution.png")


    # Imprime le rapport dans un fichier pdf
    def createReportInPdf(self,pdf_object,directory):

        text = "ANALYSE GLOBALE DU COMPTE POUR L'ANNEE"
        pdf_object.addChapterTitle(text,BLUE_TITLE_RGB[0],BLUE_TITLE_RGB[1],BLUE_TITLE_RGB[2])

        total_salaries_for_year = self.getTotalSalaryForYear()
        total_spent_for_year = self.getTotalSpent(MAIN_ACCOUNT)
        text = "- Somme totale des salaires nets pour l'année: " + str(total_salaries_for_year) + " " + chr(128)
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        text = "- Somme totale des dépenses sur l'année: " + str(total_spent_for_year) + " " + chr(128)
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
       
        text = "- Delta entre le total des salaires et le total des dépenses: "
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2],False)
        delta = round(total_salaries_for_year - total_spent_for_year, 2)
        text = str(delta) + " " + chr(128)

        if delta > 0:
            pdf_object.addText(text,GREEN_RGB[0],GREEN_RGB[1],GREEN_RGB[2])
        else:
            pdf_object.addText(text,RED_RGB[0],RED_RGB[1],RED_RGB[2])
           
    
        categories_amount = self.getTotalSpentPerCategory(MAIN_ACCOUNT)
        text = "Dépenses par catégorie sur l'année:"
        pdf_object.ln(4)
        pdf_object.addSubTitle(text,BLUE_SUBTITLE_RGB[0],BLUE_SUBTITLE_RGB[1],BLUE_SUBTITLE_RGB[2])
        for key, value in categories_amount.items():
            percentage = round((value * 100) / total_spent_for_year, 2)
            text = TAB + key + ": " + str(value) + " " + chr(128) + " (soit " + str(percentage) + " " + chr(37) + " des dépenses totales)"
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
           
        pdf_object.add_page()
        recipient_amount = self.getAmountByRecipient(MAIN_ACCOUNT)
        text = "Total des dépenses par bénéficiaire sur l'année: "
        pdf_object.ln(4)
        pdf_object.addSubTitle(text,BLUE_SUBTITLE_RGB[0],BLUE_SUBTITLE_RGB[1],BLUE_SUBTITLE_RGB[2])
        for key, value in recipient_amount.items():
            text = TAB + key + ": " + str(value) + " " + chr(128)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
         
        pdf_object.add_page()
        text = "ANALYSE GLOBALE DU COMPTE PAR MOIS"
        pdf_object.addChapterTitle(text,BLUE_TITLE_RGB[0],BLUE_TITLE_RGB[1],BLUE_TITLE_RGB[2])
        
        month_list_amount = []
        for month in self.month_list:
            month_spent = round(self.getTotalSpent(MAIN_ACCOUNT,month),2)
            month_list_amount.append(month_spent)
            text = TAB + "Dépense totale pour le mois de " + MONTH_DICT[month] + ": " + str(month_spent) + " " + chr(128)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            
        pdf_object.ln(4)
        
        for month in self.month_list:
            text = "Dépenses par catégorie pour le mois de " + MONTH_DICT[month]+ ":"
            pdf_object.addSubTitle(text,BLUE_SUBTITLE_RGB[0],BLUE_SUBTITLE_RGB[1],BLUE_SUBTITLE_RGB[2])
            categories_amount = self.getTotalSpentPerCategory(MAIN_ACCOUNT, month)
            for key, value in categories_amount.items():
                percentage = round((value * 100) / round(self.getTotalSpent(MAIN_ACCOUNT,month),month), 2)
                text = TAB + key + ": " + str(value) + " " + chr(128) + " (soit " + str(percentage) + " " + chr(37) + " des dépenses totales)"
                pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
                
            pdf_object.ln(2)
         
        pdf_object.add_page()
        
        for month in self.month_list:
            text = "Total des dépenses par bénéficiaire pour le mois de " + MONTH_DICT[month] + ": "
            pdf_object.addSubTitle(text,BLUE_SUBTITLE_RGB[0],BLUE_SUBTITLE_RGB[1],BLUE_SUBTITLE_RGB[2])
            recipient_amount = self.getAmountByRecipient(MAIN_ACCOUNT,month)
            for key, value in recipient_amount.items():
                text = TAB + key + ": " + str(value) + " " + chr(128)
                pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            
            pdf_object.ln(3)
        
        pdf_object.add_page()
        x_values = self.months_labels
        y_values = month_list_amount
        self.util.createDiagram(x_values, y_values, "Mois", "Montant en €", "Evolution des dépenses globales par mois", True, directory + "spent_evolution.png")
        picture_path = directory + "spent_evolution.png"
        pdf_object.addPicture(picture_path,720/4,720/5)
        pdf_object.add_page()
            

       