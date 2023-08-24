#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:19:06 2021

@author: wells

Classe utilitaire
"""
import pandas as pd
import matplotlib.pyplot as plt

CATEGORY_COLUMN = "category"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"
MONTH_COLUMN = "month"
IDGROUP_COLUMN = "idgroup"
ID_COLUMN = "id"
ID_TRANNSACTION_COLUMN = "idtransaction"
BOOKMARKED_COLUMN = "bookmarked"
SIGN_COLUMN = "sign"
UNIT_COLUMN = "unit"
QUANTITY_COLUMN = "quantity"
NUMBER_COLUMN = "number"

class Util():
    
    # dataframe: le dataframe sur lequel on applique le remplacement
    # replacement_data: la donnée de remplacement de la valeur NaN
    def replaceNaNValues(self,dataframe, replacement_data):
        
        if (not(dataframe is None)) & (not dataframe.empty):
            return dataframe.fillna(replacement_data)
        else:
            return None
    
    
    # Permet de formater le dataframe pour la catégorie passée en paramètres
    def getFormatedDataFrameForCategory(self,dataframe, category):
        if not(dataframe is None) & (not dataframe.empty):
            # Filtre sur la gatégorie loisir
            formated_dataframe = dataframe[dataframe[CATEGORY_COLUMN].str.contains(category,regex=False)]
            # Récupération des valeurs négatives qui correpondent à une dépense
            formated_dataframe = formated_dataframe[formated_dataframe[AMOUNT_COLUMN] < 0]
            # Suppression des -
            formated_dataframe[AMOUNT_COLUMN] = formated_dataframe[AMOUNT_COLUMN] * (-1)
            # Conversion de la colonne date en datetime
            formated_dataframe[DATE_COLUMN] = pd.to_datetime(formated_dataframe[DATE_COLUMN])
            # Ajout de la colonne month
            formated_dataframe[MONTH_COLUMN] = formated_dataframe[DATE_COLUMN].dt.month

            
            return formated_dataframe
        else:
            return None
    
    # Récupère la liste des mois
    def getListMonths(self, dataframe):
        if not(dataframe is None) & (not dataframe.empty):
            # Conversion de la colonne date en datetime
            dataframe[DATE_COLUMN] = pd.to_datetime(dataframe[DATE_COLUMN])
            # Ajout de la colonne month
            dataframe[MONTH_COLUMN] = dataframe[DATE_COLUMN].dt.month
            return dataframe[MONTH_COLUMN].unique()
        else:
            return []
        
    
    # Récupère la liste des catégories
    def getListCategories(self, dataframe):
        if not(dataframe is None) & (not dataframe.empty):
            list_categories = []
            categories_and_subcategories = dataframe[CATEGORY_COLUMN].unique()
            for cat in categories_and_subcategories:
                # on supprime les sous-catégories
                retrieved_category = ""
                if cat != "Unknown":
                    if (">" in cat):
                        index = cat.find('>')
                        retrieved_category = cat[0:index-1]
                    else:
                        retrieved_category = cat
                        
                    if retrieved_category not in list_categories:
                        list_categories.append(retrieved_category)
            return list_categories
        else:
            return []
    
    # Créé un diagramme
    def createDiagram(self, x_values, y_values, x_label, y_label, title, save_to_file, filename):
        plt.plot(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if save_to_file:
            plt.savefig(filename)
        else:
            plt.show()
        plt.close()
        
    # Vérifie l'intégrité du dataframe
    def checkDataFrame(self,dataframe):
        return not(dataframe is None) & (not dataframe.empty)
    
    # Supprime la liste des colonnes
    def dropUselessColumns(self, dataframe):
        dataframe = dataframe.drop(columns=[IDGROUP_COLUMN, ID_COLUMN, ID_TRANNSACTION_COLUMN, BOOKMARKED_COLUMN, SIGN_COLUMN, UNIT_COLUMN, QUANTITY_COLUMN, NUMBER_COLUMN], inplace=False)
        return dataframe
        