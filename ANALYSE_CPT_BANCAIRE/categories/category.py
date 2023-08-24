#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:23:39 2021

@author: wells
Classe gérant les catégories
"""

import random
import numpy as np
from util.util import Util
from pandas import Series
from pandas import DataFrame

CATEGORY_COLUMN = "category"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"
MONTH_COLUMN = "month"

BLACK_RGB = (0,0,0)
TAB = "  - "
TAB_2 = "  . "

MONTH_DICT = {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Aout", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}

class Category:
    
    category_dataframe = None
    months_labels = []
    util = Util()
    months_list = []
    category_name = ""
    
    def __init__(self, dataframe, category):
        
        if self.util.checkDataFrame(dataframe):
            # Liste des mois
            self.months_list = []
            self.months_list = dataframe[MONTH_COLUMN].unique()
            self.category_dataframe = self.util.getFormatedDataFrameForCategory(dataframe, category)
            self.category_name = category
            
            # Suppression des colonnes inutiles
            self.category_dataframe = self.util.dropUselessColumns(self.category_dataframe)
            
            # Récupération des labels des mois
            self.months_labels = []
            for m in self.months_list:
                self.months_labels.append(MONTH_DICT[m])
            
            file_name = "data_frame/" + self.category_name + "_dataframe.txt"
            file = open(file_name, "w")
            df_str = DataFrame.to_string(self.category_dataframe)
            file.write(df_str)
            file.close()
    
    
    # Retourne la dépense la plus haute pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getMaxAmount(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        max_amount = 0
        if self.util.checkDataFrame(self.category_dataframe):
            
            if month > 0:
                max_amount = self.category_dataframe[self.category_dataframe[MONTH_COLUMN] == month][AMOUNT_COLUMN].max()
                max_amount = round(max_amount,2)
            else:
                max_amount = round(self.category_dataframe[AMOUNT_COLUMN].max(),2)
        
        return max_amount
    
    # Retourne la dépense totale pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalSpentAmount(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        sum_amount = 0
        if self.util.checkDataFrame(self.category_dataframe):
            if month > 0:
                sum_amount = self.category_dataframe[self.category_dataframe[MONTH_COLUMN] == month][AMOUNT_COLUMN].sum()
                sum_amount = round(sum_amount, 2)
            else:
                sum_amount = round(self.category_dataframe[AMOUNT_COLUMN].sum(),2)
            
        return sum_amount
    
    # Retourne la liste du montants des dépenses par mois
    def getListTotalAmountForMonths(self):
        if self.util.checkDataFrame(self.category_dataframe):
            month_list_amount = []
            for month in self.months_list:
                total_month_amount = self.getTotalSpentAmount(month)
                month_list_amount.append(total_month_amount)
            
            return month_list_amount
        else:
            return []
    
    
    # Retourne un dictionnaire contenant le montant de chaque sous catégorie pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalAmountPerSubCategory(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        sub_categories_amount = dict()
        if self.util.checkDataFrame(self.category_dataframe):
            sub_cats = self.category_dataframe[CATEGORY_COLUMN].unique()
            
            if month > 0:
                for sc in sub_cats:
                    tmp_dataframe = self.category_dataframe[(self.category_dataframe[CATEGORY_COLUMN] == sc) & (self.category_dataframe[MONTH_COLUMN] == month)]
                    cat_total_amount = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                    sub_categories_amount[sc] = cat_total_amount
            else:
                for sc in sub_cats:
                    tmp_dataframe = self.category_dataframe[self.category_dataframe[CATEGORY_COLUMN] == sc]
                    cat_total_amount = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                    sub_categories_amount[sc] = cat_total_amount
        
        return sub_categories_amount

    
    # Retourne un dictionnaire contenant le montant de chaque sous catégorie en pourcentage pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalAmountPerSubCategoryInPercent(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        sub_categories_amount = dict()
        if self.util.checkDataFrame(self.category_dataframe):
            sub_cats = self.category_dataframe[CATEGORY_COLUMN].unique()
            
            if month > 0:
                total_categories = self.getTotalSpentAmount(month)
                for sc in sub_cats:
                    tmp_dataframe = self.category_dataframe[(self.category_dataframe[CATEGORY_COLUMN] == sc) & (self.category_dataframe[MONTH_COLUMN] == month)]
                    cat_total_amount = tmp_dataframe[AMOUNT_COLUMN].sum()
                    if total_categories != 0.0:
                        cat_total_in_percent = (cat_total_amount * 100)/total_categories
                    else:
                        cat_total_in_percent = 0.0
                    sub_categories_amount[sc] = round(cat_total_in_percent,2)
            else:
                total_categories = self.getTotalSpentAmount()
                for sc in sub_cats:
                    tmp_dataframe = self.category_dataframe[self.category_dataframe[CATEGORY_COLUMN] == sc]
                    cat_total_amount = tmp_dataframe[AMOUNT_COLUMN].sum()
                    if total_categories != 0.0:
                        cat_total_in_percent = (cat_total_amount * 100)/total_categories
                    else:
                        cat_total_in_percent = 0.0
                    sub_categories_amount[sc] = round(cat_total_in_percent,2)
        
        return sub_categories_amount
    
    
    
    
    
    # Retourne l'écart type pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalDeviation(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        deviation = 0.0 
        if self.util.checkDataFrame(self.category_dataframe):
            
            if month > 0:
               tmp_dataframe = self.category_dataframe[self.category_dataframe[MONTH_COLUMN] == month]
               deviation = round(np.std(tmp_dataframe[AMOUNT_COLUMN]),2)
            else:
               deviation = round(np.std(self.category_dataframe[AMOUNT_COLUMN]),2) 
        
        return deviation
    
    # Retourne les statistiques de la colonne amount pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    # Affiche le résultat dans la console ou l'enregistre dans un fichier
    def getStats(self,file,month=0,is_file=True):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        if self.util.checkDataFrame(self.category_dataframe):
            
            if month > 0:
                tmp_dataframe = self.category_dataframe[self.category_dataframe[MONTH_COLUMN] == month]
                if is_file:
                    file.write(Series.to_string(tmp_dataframe[AMOUNT_COLUMN].describe())+"\n")
                else:
                    print(Series.to_string(tmp_dataframe[AMOUNT_COLUMN].describe()))
            else:
                if is_file:
                    file.write(Series.to_string(self.category_dataframe[AMOUNT_COLUMN].describe())+"\n")
                else:
                    print(Series.to_string(self.category_dataframe[AMOUNT_COLUMN].describe())+"\n")
                    
    
    # Retourne les statistiques de la colonne amount pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    # Enregistre le résultat dans un fichier pdf
    def getStatsForPdf(self,pdf_object,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        if self.util.checkDataFrame(self.category_dataframe) and not(pdf_object is None):
            
            if month > 0:
                tmp_dataframe = self.category_dataframe[self.category_dataframe[MONTH_COLUMN] == month]
                stats_series = tmp_dataframe[AMOUNT_COLUMN].describe()
                for index, value in stats_series.items():
                    text = "   " + TAB_2 + index + ": " + str(round(value,2))
                    pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            else:
                stats_series = self.category_dataframe[AMOUNT_COLUMN].describe()
                for index, value in stats_series.items():
                    text = "   " + TAB_2 + index + ": " + str(round(value,2))
                    pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
                
    
    # Créer et enregistre le rapport dans un fichier
    def createReport(self,file,directory):
        
        message_head = "- CATEGORIE " + self.category_name.upper() + ": "
        month_list_amount = []
        
        title = "Rapport de l'analyse de la catégorie " + self.category_name
        file.write(title.upper()+"\n")
        file.write("---------------------------------------------"+"\n"+"\n")
        
        
        # DEPENSES TOTALES ET MAX
        file.write("Dépenses totales et max: " + "\n")
        total_amount_year = self.getTotalSpentAmount()
        file.write(message_head + "Montant total des dépenses pour l'année: " + str(total_amount_year) + " €"+"\n")
        max_amount_year = self.getMaxAmount()
        file.write(message_head + "Plus haute dépense pour l'année: " + str(max_amount_year) + " €"+"\n"+"\n")
        
        for month in self.months_list:
            total_month_amount = self.getTotalSpentAmount(month)
            max_for_month = self.getMaxAmount(month)
            month_list_amount.append(total_month_amount)
            file.write(message_head + "Dépense totale pour le mois de " + MONTH_DICT[month] + ": " + str(total_month_amount) + " €"+"\n")
            file.write(message_head + "Plus haute dépense pour le mois de " + MONTH_DICT[month] + ": " + str(max_for_month) + " €"+"\n"+"\n")
            
            
        # DEPENSES PAR CATEGORIE EN €
        file.write("Dépenses par sous-catégories en €: " + "\n")
        amount_sub_categories_year = self.getTotalAmountPerSubCategory()
        file.write(message_head + "Dépenses par sous-catégorie pour l'année: "+"\n")
        for key, value in amount_sub_categories_year.items():
            file.write("\t" + key + ": " + str(value) + " €"+"\n")
        file.write("\n")
            
        for month in self.months_list:
            categories_amount_dict = self.getTotalAmountPerSubCategory(month)
            file.write(message_head + "Dépenses par sous-catégorie pour le mois de " + MONTH_DICT[month]+ ":" + "\n")
            for key, value in categories_amount_dict.items():
                file.write("\t" + key + ": " + str(value) + " €"+"\n")
            file.write("\n")
        
        
        # DEPENSES PAR CATEGORIE EN %
        file.write("Dépenses par sous-catégories en %: " + "\n")
        amount_sub_categories_year = self.getTotalAmountPerSubCategoryInPercent()
        file.write(message_head + "Dépenses par sous-catégorie pour l'année: "+"\n")
        for key, value in amount_sub_categories_year.items():
            file.write("\t" + key + ": " + str(value) + " %"+"\n")
        file.write("\n")
            
        for month in self.months_list:
            categories_amount_dict = self.getTotalAmountPerSubCategoryInPercent(month)
            file.write(message_head + "Dépenses par sous-catégorie pour le mois de " + MONTH_DICT[month]+ ":" + "\n")
            for key, value in categories_amount_dict.items():
                file.write("\t" + key + ": " + str(value) + " %"+"\n")
            file.write("\n")
            
        
        # STATISTIQUES DE LA CATEGORIE
        file.write("Statistiques: " + "\n")
        file.write(message_head + "Statistiques pour l'année:" + "\n")
        self.getStats(file)
        file.write("\n")
        
        for month in self.months_list:
            file.write(message_head + "Statistiques pour le mois de: " + MONTH_DICT[month]+ ":" + "\n")
            self.getStats(file,month)
            file.write("\n")
            
        
        # ECART TYPE
        file.write("Ecart type: " + "\n")
        deviation_year = self.getTotalDeviation()
        file.write(message_head + "écart type:" + "\n")
        file.write("\t" + "pour l'année: " + str(deviation_year) + "\n")
        
        for month in self.months_list:
            deviation_month = self.getTotalDeviation(month)
            file.write("\t" + "pour " + MONTH_DICT[month] + ": " + str(deviation_month) + "\n")
        
        file.write("\n")
        
        
        # GAPHIQUE
        file_name = directory + self.category_name.lower() + "_evolution.png"
        title = "Evolution des dépenses de la catégorie " + self.category_name.lower() + " par mois"
        x_values = self.months_labels
        y_values = month_list_amount
        self.util.createDiagram(x_values, y_values, "Mois", "Montant en €", title, True, file_name)
        
    
    # Imprime le rapport dans un fichier pdf
    def createReportInPdf(self,pdf_object,directory):
        
        month_list_amount = []
        
        text = "ANALYSE DE LA CATEGORIE " + self.category_name.upper() + " POUR L'ANNEE"
        red_value = random.randint(0, 255)
        green_value = random.randint(0, 255)
        blue_value = random.randint(0, 255)
        pdf_object.addChapterTitle(text,red_value,green_value,blue_value)
        
        
        # DEPENSES TOTALES ET MAX
        text = "Dépenses totales et max: "
        total_amount_year = self.getTotalSpentAmount()
        pdf_object.addSubTitle(text,red_value+20,green_value+20,blue_value)
        text = TAB + "Montant total des dépenses pour l'année: " + str(total_amount_year) + " " + chr(128)
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        
        max_amount_year = self.getMaxAmount()
        text = TAB + "Plus haute dépense pour l'année: " + str(max_amount_year) + " " + chr(128)
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        pdf_object.ln()
        
        for month in self.months_list:
            total_month_amount = self.getTotalSpentAmount(month)
            max_for_month = self.getMaxAmount(month)
            month_list_amount.append(total_month_amount)
            text = TAB + "Dépense totale pour le mois de " + MONTH_DICT[month] + ": " + str(total_month_amount) + " " + chr(128)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            text = TAB + "Plus haute dépense pour le mois de " + MONTH_DICT[month] + ": " + str(max_for_month) + " " + chr(128)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            pdf_object.ln()
            
        pdf_object.ln(1)
        
    
        # DEPENSES PAR CATEGORIE EN €
        text = "Dépenses par sous-catégories en " + chr(128)
        pdf_object.addSubTitle(text,red_value+20,green_value+20,blue_value)
        text = TAB + "Dépenses par sous-catégorie pour l'année: "
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        amount_sub_categories_year = self.getTotalAmountPerSubCategory()
        
        for key, value in amount_sub_categories_year.items():
            text = "   " + TAB_2 + key + ": " + str(value) + " " + chr(128)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        pdf_object.ln()
            
        for month in self.months_list:
            categories_amount_dict = self.getTotalAmountPerSubCategory(month)
            text = TAB + "Dépenses par sous-catégorie pour le mois de " + MONTH_DICT[month]+ ":"
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            for key, value in categories_amount_dict.items():
                text = "   " + TAB_2 + key + ": " + str(value) + " " + chr(128)
                pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            pdf_object.ln()
        pdf_object.ln()
        
        
        # DEPENSES PAR CATEGORIE EN %
        text = "Dépenses par sous-catégories en " + chr(37) + ": "
        pdf_object.addSubTitle(text,red_value+20,green_value+20,blue_value)
        text = TAB + "Dépenses par sous-catégorie pour l'année: "
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        amount_sub_categories_year = self.getTotalAmountPerSubCategoryInPercent()
        for key, value in amount_sub_categories_year.items():
            text = "   " + TAB_2  + key + ": " + str(value) + " " + chr(37)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        pdf_object.ln()
            
        for month in self.months_list:
            categories_amount_dict = self.getTotalAmountPerSubCategoryInPercent(month)
            text = TAB + "Dépenses par sous-catégorie pour le mois de " + MONTH_DICT[month]+ ":"
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            for key, value in categories_amount_dict.items():
                text = "   " + TAB_2  + key + ": " + str(value) + " " + chr(37)
                pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            pdf_object.ln()
        pdf_object.ln()
        
        
        # STATISTIQUES DE LA CATEGORIE
        text = "Statistiques des dépenses:"
        pdf_object.addSubTitle(text,red_value+20,green_value+20,blue_value)
        text = TAB + "Statistiques pour l'année:"
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        self.getStatsForPdf(pdf_object)
        pdf_object.ln()
        
        for month in self.months_list:
            text = TAB + "Statistiques pour le mois de " + MONTH_DICT[month]+ ":"
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
            self.getStatsForPdf(pdf_object,month)
            pdf_object.ln()
        
        # ECART TYPE
        text = "Ecart type: "
        pdf_object.addSubTitle(text,red_value+20,green_value+20,blue_value)
        deviation_year = self.getTotalDeviation()
        text = TAB + "écart type pour l'année: " + str(deviation_year)
        pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        
        for month in self.months_list:
            deviation_month = self.getTotalDeviation(month)
            text = TAB + "écart type pour le mois de " + MONTH_DICT[month] + ": " + str(deviation_month)
            pdf_object.addText(text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
        
        pdf_object.ln(5)
        
        # GAPHIQUE
        file_name = directory + self.category_name.lower() + "_evolution.png"
        title = "Evolution des dépenses de la catégorie " + self.category_name.lower() + " par mois"
        x_values = self.months_labels
        y_values = month_list_amount
        self.util.createDiagram(x_values, y_values, "Mois", "Montant en €", title, True, file_name)
        pdf_object.addPicture(file_name,720/4,720/5)
        pdf_object.add_page()

