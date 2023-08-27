#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:03:28 2022

@author: Jocelyn GIROD
Helper pour l'analyse des requêtes.
"""
import pandas as pd

class RequestHelper():
    
    COLUMN_USER_EXPERIENCE = 'User Experience'
    COLUMN_TIME = 'Time'
    COLUMN_EXEC_TIME = "Exe Time (ms)"
    COLUMN_LATENCY = 'End to End Latency Time (ms)'
    COLUMN_URL = 'URL'
    COLUMN_BUSINESS_TRANSACTION = 'Business Transaction'
    COLUMN_TIER = 'Tier'
    COLUMN_NODE = 'Node'
    COLUMN_ARCHIVED = 'Archived'
    
    """Récupère les valeurs répétées ainsi que leur nombre de répétition.
    :param dataColumn: la colonne contenant les donnéees.
    :type dataColumn: une Serie Panda.
    :returns:: un dictionnaire dans la clé est la valeur et la donnée le nombre de répétitions.
    :rtype: dictionnaire.
    """
    def extractRepeatedValue(self, dataColumn):
        
        if not isinstance(dataColumn, pd.Series):
            print("Error: dataColumn is not a Pandas Serie !")
            return
        
        dictionaryRepeatedValues = {}
        if (not(dataColumn is None)) & (not dataColumn.empty):
            for timeToCompare in dataColumn:
                occurrence = 0
                for time in dataColumn:
                    if(timeToCompare == time):
                        occurrence = occurrence + 1
                
                if (occurrence > 1):
                    dictionaryRepeatedValues[timeToCompare] = occurrence
                    
        return dictionaryRepeatedValues
    