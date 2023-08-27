#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:03:28 2022

@author: Jocelyn GIROD
Helper pour l'analyse des requêtes.
"""
import pandas as pd


class RequestHelper:
    COLUMN_USER_EXPERIENCE = 'User Experience'
    COLUMN_TIME = 'Time'
    COLUMN_EXEC_TIME = "Exe Time (ms)"
    COLUMN_LATENCY = 'End to End Latency Time (ms)'
    COLUMN_URL = 'URL'
    COLUMN_BUSINESS_TRANSACTION = 'Business Transaction'
    COLUMN_TIER = 'Tier'
    COLUMN_NODE = 'Node'
    COLUMN_ARCHIVED = 'Archived'

    # Couleurs
    BLACK_RGB = (0, 0, 0)
    BLUE_RGB = (14, 65, 215)
    BLUE_LIGHT_RGB = (2, 54, 73)
    GREEN_RGB = (14, 99, 10)

    """Récupère les valeurs répétées ainsi que leur nombre de répétition.
    :param dataColumn: la colonne contenant les donnéees.
    :type dataColumn: une Serie Panda.
    :returns:: un dictionnaire dans la clé est la valeur et la donnée le nombre de répétitions.
    :rtype: dictionnaire.
    """

    @staticmethod
    def extractRepeatedValue(dataColumn):

        if not isinstance(dataColumn, pd.Series):
            print("Error: dataColumn is not a Pandas Serie !")
            return

        dictionaryRepeatedValues = {}
        if (not (dataColumn is None)) & (not dataColumn.empty):
            for timeToCompare in dataColumn:
                occurrence = dataColumn.value_counts()[timeToCompare]
                if occurrence > 1:
                    if timeToCompare not in dictionaryRepeatedValues.keys():
                        dictionaryRepeatedValues[timeToCompare] = occurrence

        return dictionaryRepeatedValues

    """Retourne la valeur qui a la plus haute fréquence
    dans la série passée en pramètre.
    :param dataColumn: la colonne contenant les doonnées.
    :type dataColumn: une série Pandas.
    :returns: un tableau contenant le couple nombre de répétitions (indexe 0), valeur (index 1).
    :rtype: une tableau. 
    """

    def getHighFrequency(self, dataColumn):

        if not isinstance(dataColumn, pd.Series):
            print("Error: dataColumn is not a Pandas Serie !")
            return

        dictionaryRepeatedValues = self.extractRepeatedValue(dataColumn)
        highValue = 0
        keyHighValue = 0.0
        for key in dictionaryRepeatedValues.keys():
            value = dictionaryRepeatedValues.get(key)
            if value > highValue:
                highValue = value
                keyHighValue = key

        arrayHighFrequency = [highValue, keyHighValue]
        return arrayHighFrequency
