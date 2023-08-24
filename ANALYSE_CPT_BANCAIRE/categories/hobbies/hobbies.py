#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:31:33 2021

@author: wells

Classe gérant la catégorie Loisirs
"""

import numpy as np
from util.util import Util
from pandas import Series

CATEGORY_COLUMN = "category"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"
MONTH_COLUMN = "month"

MONTH_DICT = {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Aout", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}

class Hobbies():
    hobbies_dataframe = None
    months_labels = []
    util = Util()
    months_list = []
    def __init__(self, dataframe):
        
        if self.util.checkDataFrame(dataframe):
            self.hobbies_dataframe = self.util.getFormatedDataFrameForCategory(dataframe, "Loisirs")
            # Suppression des colonnes inutiles
            self.hobbies_dataframe = self.util.dropUselessColumns(self.hobbies_dataframe)
            months = self.hobbies_dataframe[MONTH_COLUMN].unique()
            for m in months:
                self.months_labels.append(MONTH_DICT[m])
            
            self.months_list = self.hobbies_dataframe[MONTH_COLUMN].unique()
            
    
    # Retourne la dépense la plus haute pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getMaxAmount(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        max_amount = 0
        if self.util.checkDataFrame(self.hobbies_dataframe):
            
            if month > 0:
                max_amount = self.hobbies_dataframe[self.hobbies_dataframe[MONTH_COLUMN] == month][AMOUNT_COLUMN].max()
                max_amount = round(max_amount,2)
            else:
                max_amount = round(self.hobbies_dataframe[AMOUNT_COLUMN].max(),2)
        
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
        if self.util.checkDataFrame(self.hobbies_dataframe):
            if month > 0:
                sum_amount = self.hobbies_dataframe[self.hobbies_dataframe[MONTH_COLUMN] == month][AMOUNT_COLUMN].sum()
                sum_amount = round(sum_amount, 2)
            else:
                sum_amount = round(self.hobbies_dataframe[AMOUNT_COLUMN].sum(),2)
            
        return sum_amount
            
        
    # Retourne la liste du montant des dépenses par mois
    def getListTotalAmountForMonths(self):
        month_list_amount = []
        for month in self.months_list:
            total_month_amount = self.getTotalSpentAmount(month)
            month_list_amount.append(total_month_amount)
        
        return month_list_amount
            
        
    # Retourne un dictionnaire contenant le montant de chaque sous catégorie pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getTotalAmountPerSubCategory(self,month=0):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        sub_categories_amount = dict()
        if self.util.checkDataFrame(self.hobbies_dataframe):
            sub_cats = self.hobbies_dataframe[CATEGORY_COLUMN].unique()
            
            if month > 0:
                for sc in sub_cats:
                    tmp_dataframe = self.hobbies_dataframe[(self.hobbies_dataframe[CATEGORY_COLUMN] == sc) & (self.hobbies_dataframe[MONTH_COLUMN] == month)]
                    cat_total_amount = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                    sub_categories_amount[sc] = cat_total_amount
            else:
                for sc in sub_cats:
                    tmp_dataframe = self.hobbies_dataframe[self.hobbies_dataframe[CATEGORY_COLUMN] == sc]
                    cat_total_amount = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                    sub_categories_amount[sc] = cat_total_amount
        
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
        if self.util.checkDataFrame(self.hobbies_dataframe):
            
            if month > 0:
               tmp_dataframe = self.hobbies_dataframe[self.hobbies_dataframe[MONTH_COLUMN] == month]
               deviation = round(np.std(tmp_dataframe[AMOUNT_COLUMN]),2)
            else:
               deviation = round(np.std(self.hobbies_dataframe[AMOUNT_COLUMN]),2) 
        
        return deviation
    
    
    
    # Retourne les statistiques de la colonne amount pour:
    # l'année si month n'est pas renseigné ou si month <= 0
    # le mois (1: janvier, 2: février, 3:mars, etc...)
    def getStats(self,file,month=0,is_file=True):
        try:
            month = int(month)
        except:
            print(f"Erreur le mois renseigné ({month}) n'a pas un format correct.")
        
        if self.util.checkDataFrame(self.hobbies_dataframe):
            
            if month > 0:
                tmp_dataframe = self.hobbies_dataframe[self.hobbies_dataframe[MONTH_COLUMN] == month]
                if is_file:
                    file.write(Series.to_string(tmp_dataframe[AMOUNT_COLUMN].describe())+"\n")
                else:
                    print(Series.to_string(tmp_dataframe[AMOUNT_COLUMN].describe()))
            else:
                if is_file:
                    file.write(Series.to_string(self.hobbies_dataframe[AMOUNT_COLUMN].describe())+"\n")
                else:
                    print(Series.to_string(self.hobbies_dataframe[AMOUNT_COLUMN].describe())+"\n")
        
    
    
    # Affiche le rapport
    def printReport(self,file):
        file.write("Rapport de l'analyse de la catégorie Loisirs".upper()+"\n")
        file.write("---------------------------------------------"+"\n"+"\n")
        
        total_amount_year = self.getTotalSpentAmount()
        file.write("- CATEGORIE LOISIRS: Montant total des dépenses pour l'année: " + str(total_amount_year) + " €"+"\n")
        max_amount_year = self.getMaxAmount()
        file.write("- CATEGORIE LOISIRS: Plus haute dépense pour l'année: " + str(max_amount_year) + " €"+"\n"+"\n")
        
        amount_categories_year = self.getTotalAmountPerSubCategory()
        file.write("- CATEGORIE LOISIRS: Dépenses par sous-catégorie pour l'année: "+"\n")
        for key, value in amount_categories_year.items():
            file.write("\t" + key + ": " + str(value) + " €"+"\n")
            
        file.write("\n")
            
        month_list_amount = []
        for month in self.months_list:
            total_month_amount = self.getTotalSpentAmount(month)
            max_for_month = self.getMaxAmount(month)
            month_list_amount.append(total_month_amount)
            file.write("- CATEGORIE LOISIRS: Dépense totale pour le mois de " + MONTH_DICT[month] + ": " + str(total_month_amount) + " €"+"\n")
            file.write("- CATEGORIE LOISIRS: Plus haute dépense pour le mois de " + MONTH_DICT[month] + ": " + str(max_for_month) + " €"+"\n"+"\n")
            
            
        for month in self.months_list:
            categories_amount_dict = self.getTotalAmountPerSubCategory(month)
            file.write("CATEGORIE LOISIRS: Dépenses par sous-catégorie pour le mois de " + MONTH_DICT[month]+ ":" + "\n")
            for key, value in categories_amount_dict.items():
                file.write("\t" + key + ": " + str(value) + " €"+"\n")
            file.write("\n")
            
        file.write("\n")
        
        file.write("Statistiques pour l'année:" + "\n")
        self.getStats(file)
        for month in self.months_list:
            file.write("Statistiques pour le mois de: " + MONTH_DICT[month]+ ":" + "\n")
            self.getStats(file,month)
            file.write("\n")
            
        deviation_year = self.getTotalDeviation()
        file.write("CATEGORIE LOISIRS: écart type:" + "\n")
        file.write("\t" + "pour l'année: " + str(deviation_year) + "\n")
        for month in self.months_list:
            deviation_month = self.getTotalDeviation(month)
            file.write("\t" + "pour " + MONTH_DICT[month] + ": " + str(deviation_month) + "\n")
            
            
        x_values = self.months_labels
        y_values = month_list_amount
        self.util.createDiagram(x_values, y_values, "Mois", "Montant en €", "Evolution des dépenses de la catégorie Loisir par mois", True, "report/hobbies_evolution.png")
        
    
        