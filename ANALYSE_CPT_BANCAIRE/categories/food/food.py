#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 09:47:43 2021

@author: wells

Classe gérant la catégorie Alimentation
"""

import numpy as np
from util.util import Util
from pandas import Series

CATEGORY_COLUMN = "category"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"
MONTH_COLUMN = "month"

MONTH_DICT = {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Aout", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}

class Food():
    food_dataframe = None
    months_labels = []
    util = Util()
    months_list = []
    
    def __init__(self, dataframe):
        if (not(dataframe is None)) & (not dataframe.empty):
            self.food_dataframe = self.util.getFormatedDataFrameForCategory(dataframe, "Alimentation")
            # Suppression des colonnes inutiles
            self.food_dataframe = self.util.dropUselessColumns(self.food_dataframe)
            months = self.food_dataframe[MONTH_COLUMN].unique()
            for m in months:
                self.months_labels.append(MONTH_DICT[m])
            
            self.months_list = self.food_dataframe[MONTH_COLUMN].unique()
    
    
    # Retourne la dépense la plus haute de l'année
    def getMaxAmountForYear(self):
        if self.util.checkDataFrame(self.food_dataframe):
            return self.food_dataframe[AMOUNT_COLUMN].max()
        else:
            return None
        
    # Retourne la dépense la plus haute de l'année
    def getMaxAmountForMonth(self,month):
        if self.util.checkDataFrame(self.food_dataframe):
            tmp_dataframe = self.food_dataframe[self.food_dataframe[MONTH_COLUMN] == month]
            return round(tmp_dataframe[AMOUNT_COLUMN].max(),2)
        else:
            return None
    
    # Retourne le montant total pour l'année
    def getTotalAmountForYear(self):
        if self.util.checkDataFrame(self.food_dataframe):
            return round(self.food_dataframe[AMOUNT_COLUMN].sum(),2)
        else:
            return None
        
     # Retourne le montant total du mois
    def getTotalAmountForMonth(self,month):
        if self.util.checkDataFrame(self.food_dataframe):
            tmp_dataframe = self.food_dataframe[self.food_dataframe[MONTH_COLUMN] == month]
            return round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
        else:
            return None
        
    # Retourne la liste du montant des dépenses par mois
    def getListTotalAmountForMonths(self):
        month_list_amount = []
        for month in self.months_list:
            total_month_amount = self.getTotalAmountForMonth(month)
            month_list_amount.append(total_month_amount)
        
        return month_list_amount
    
    # Retourne un dictionnaire contenant le montant pour chaque sous catégorie pour l'année
    def getTotalAmountPerSubCategoryForYear(self):
        sub_categories_amount = dict()
        if self.util.checkDataFrame(self.food_dataframe):
            sub_cats = self.food_dataframe[CATEGORY_COLUMN].unique()
            
            for sc in sub_cats:
                tmp_dataframe = self.food_dataframe[self.food_dataframe[CATEGORY_COLUMN] == sc]
                cat_total_amount = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                sub_categories_amount[sc] = cat_total_amount
            
            return sub_categories_amount
        else:
            return None
        
    # Retourne un dictionnaire contenant le montant pour chaque sous catégorie pour le mois
    def getTotalAmountPerSubCategoryForMonth(self,month):
        sub_categories_amount = dict()
        if self.util.checkDataFrame(self.food_dataframe):
            sub_cats = self.food_dataframe[CATEGORY_COLUMN].unique()
            
            for sc in sub_cats:
                tmp_dataframe = self.food_dataframe[(self.food_dataframe[CATEGORY_COLUMN] == sc) & (self.food_dataframe[MONTH_COLUMN] == month)]
                cat_total_amount = round(tmp_dataframe[AMOUNT_COLUMN].sum(),2)
                sub_categories_amount[sc] = cat_total_amount
            
            return sub_categories_amount
        else:
            return None
        
    # Retourne l'écart type pour l'année
    def getTotalDeviationForYear(self):
        if self.util.checkDataFrame(self.food_dataframe):
            deviation = round(np.std(self.food_dataframe[AMOUNT_COLUMN]),2)
            return deviation
        else:
            return None
        
    # Retourne l'écart type pour le mois
    def getTotalDeviationForMonth(self,month):
        if self.util.checkDataFrame(self.food_dataframe):
            tmp_dataframe = self.food_dataframe[self.food_dataframe[MONTH_COLUMN] == month]
            deviation = round(np.std(tmp_dataframe[AMOUNT_COLUMN]),2)
            return deviation
        else:
            return None
        
    # Retourne les statistiques de la colonne amount pour l'année
    def getStatsForYear(self,file):
        if self.util.checkDataFrame(self.food_dataframe):
            file.write(Series.to_string(self.food_dataframe[AMOUNT_COLUMN].describe())+"\n")
            
    # Retourne les statistiques de la colonne amount pour le mois
    def getStatsForMonth(self,month,file):
        if self.util.checkDataFrame(self.food_dataframe):
            tmp_dataframe = self.food_dataframe[self.food_dataframe[MONTH_COLUMN] == month]
            file.write(Series.to_string(tmp_dataframe[AMOUNT_COLUMN].describe())+"\n")
            
    
    # Affiche le rapport
    def printReport(self,file):
        file.write("Rapport de l'analyse de la catégorie Alimentation".upper()+"\n")
        file.write("---------------------------------------------"+"\n"+"\n")
        
        total_amount_year = self.getTotalAmountForYear()
        file.write("- CATEGORIE ALIMENTATION: Montant total des dépenses pour l'année: " + str(total_amount_year) + " €" + "\n")
        max_amount_year = self.getMaxAmountForYear()
        file.write("- CATEGORIE ALIMENTATION: Plus haute dépense pour l'année: " + str(max_amount_year) + " €" + "\n"+"\n")
        
        amount_categories_year = self.getTotalAmountPerSubCategoryForYear()
        file.write("- CATEGORIE ALIMENTATION: Dépenses par sous-catégorie pour l'année: " + "\n")
        for key, value in amount_categories_year.items():
            file.write("\t" + key + ": " + str(value) + " €" + "\n")
            
        file.write("\n")
            
        month_list_amount = []
        for month in self.months_list:
            total_month_amount = self.getTotalAmountForMonth(month)
            max_for_month = self.getMaxAmountForMonth(month)
            month_list_amount.append(total_month_amount)
            file.write("- CATEGORIE ALIMENTATION: Dépense totale pour le mois de " + MONTH_DICT[month] + ": " + str(total_month_amount) + " €" + "\n")
            file.write("- CATEGORIE ALIMENTATION: Plus haute dépense pour le mois de " + MONTH_DICT[month] + ": " + str(max_for_month) + " €" + "\n" + "\n")
            
            
        for month in self.months_list:
            categories_amount_dict = self.getTotalAmountPerSubCategoryForMonth(month)
            file.write("CATEGORIE ALIMENTATION: Dépenses par sous-catégorie pour le mois de " + MONTH_DICT[month] + ":" + "\n")
            for key, value in categories_amount_dict.items():
                file.write("\t" + key + ": " + str(value) + " €" + "\n")
            file.write("\n")
        
        file.write("\n")
        
        for month in self.months_list:
            file.write("Statistiques pour le mois de: " + MONTH_DICT[month] + ":" + "\n")
            self.getStatsForMonth(month,file)
            file.write("\n")
        
        x_values = self.months_labels
        y_values = month_list_amount
        self.util.createDiagram(x_values, y_values, "Mois", "Montant en €", "Evolution des dépenses de la catégorie Alimentation par mois", True, "report/food_evolution.png")