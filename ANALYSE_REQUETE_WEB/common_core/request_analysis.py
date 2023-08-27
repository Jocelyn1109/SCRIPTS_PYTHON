#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 13:26:21 2022

@author: Jocelyn GIROD
Classe mère pour l'analyse des requêtes.
"""

import sys

# Ajout du répertoire Common dans le système de fichier
# pour l'import de Util et PdfReport
# NOTE: remplacer mon_compte par la vraie valeur
sys.path.append('/home/mon_compte/DEV/Python/Common/')

import pandas as pd
from helper.request_helper import RequestHelper
import numpy as np
import matplotlib.pyplot as plt


class RequestAnalysis(object):
    request_helper = RequestHelper()

    matPlt = plt
    npy = np

    # Précision des float
    floatAccuracy = 4

    # Données de l'analyse
    requestDataframe = pd.DataFrame()
    meanExecTimeTotalRequest = 0.0
    standardDeviation = 0.0
    meanMinusStandardDeviation = 0.0
    meanPlusStandardDeviation = 0.0
    threshold = 0.0
    minMaxArray = npy.empty(2, dtype=float)
    quantileArray = npy.empty(2, dtype=float)
    highFrequencyArray = []
    median = 0.0
    nbRequest = 0

    # marge pour calculer le seuil
    edge = 0.0

    rootPicturePath = './report/pictures/'

    """Constructeur"""

    def __init__(self, dataframe, nbRequest=0, edge=1.5):

        if not self._isDataFram(dataframe):
            return

        self.requestDataframe = dataframe
        self.nbRequest = nbRequest
        self.edge = edge

    """Récupère la moyenne des données d'une colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :param dataframe: le dataframe.
    :type dataframe: un dataframe Pandas.
    :returns: la moyenne.
    :rtype: float.
    """

    def getMean(self, columnName, dataframe):

        if not self._isDataFram(dataframe):
            return
        elif type(columnName) is not str:
            print("Error: columnName is not a str !")
            return
        else:
            # Calcul de la moyenne
            mean = dataframe.loc[:, columnName].astype(float).mean()
            return round(mean, self.floatAccuracy)

    """Récupère l'écart type des valeurs de la colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :param dataframe: le dataframe.
    :type dataframe: un dataframe Pandas.
    :returns: l'écart type.
    :rtype: float.
    """

    def getStandardDeviation(self, columnName, dataframe):

        if not self._isDataFram(dataframe):
            return
        elif type(columnName) is not str:
            print("Error: columnName is not a str !")
            return
        else:
            standardDeviation = dataframe[columnName].std()
            return round(standardDeviation, self.floatAccuracy)

    """Récupère la valeur min et max d'une colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :param dataframe: le dataframe.
    :type dataframe: un dataframe Pandas.
    :returns: un tableau contenant le min (indexe 0) et le max (indexe 1).
    :rtype: array
    """

    def getMinMaxValues(self, columnName, dataframe):

        minMaxArray = self.npy.empty(2, dtype=float)
        if not self._isDataFram(dataframe):
            return
        elif type(columnName) is not str:
            print("Error: columnName is not a str !")
            return
        else:
            minValue = dataframe[columnName].min()
            maxValue = dataframe[columnName].max()
            minMaxArray[0] = round(minValue, self.floatAccuracy)
            minMaxArray[1] = round(maxValue, self.floatAccuracy)

        return minMaxArray

    """Récupère le premier et le troisième quartile de la colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :param dataframe: le dataframe.
    :type dataframe: un dataframe Pandas.
    :returns: un tableau contenant le premier quartile (indexe 0) et le troisième quartile (indexe 1).
    :rtype: array
    """

    def getQuantileQ1Q3(self, columnName, dataframe):

        quantileArray = self.npy.empty(2, dtype=float)
        if not self._isDataFram(dataframe):
            return
        elif type(columnName) is not str:
            print("Error: columnName is not a str !")
            return
        else:
            # Premier quartile de la série
            q1 = dataframe[columnName].quantile(0.25)
            # Trooisième quartile de la série
            q3 = dataframe[columnName].quantile(0.75)
            quantileArray[0] = round(q1, self.floatAccuracy)
            quantileArray[1] = round(q3, self.floatAccuracy)

        return quantileArray

    """Récupère la médiane de la colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :param dataframe: le dataframe.
    :type dataframe: un dataframe Pandas.
    :returns: la médiane.
    :rtype: un float.
    """

    def getMedian(self, columnName, dataframe):

        if not self._isDataFram(dataframe):
            return
        elif type(columnName) is not str:
            print("Error: columnName is not a str !")
            return
        else:
            median = dataframe[columnName].median()
            return round(median, self.floatAccuracy)

    """Retourne la valeur qui a la plus haute fréquence
    dans la série passée en pramètre.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :param dataframe: le dataframe.
    :type dataframe: un dataframe Pandas.
    :returns: un tableau contenant le couple nombre de répétitions (indexe 0), valeur (index 1).
    :rtype: une tableau. 
    """

    def getHighFrequency(self, columnName, dataframe):

        if not self._isDataFram(dataframe):
            return
        elif type(columnName) is not str:
            print("Error: columnName is not a str !")
            return
        else:

            serie = dataframe[columnName]
            return self.request_helper.getHighFrequency(serie)

    """Valide si ou ou non la variable datafram est un dataFrame Pandas.
    :param dataframe: le dataframe à vérifier.
    :type dataframe: un dataframe Panda.
    :returns: True si c'est un DataFrame sinon False
    :rtype: booléen
    """

    @staticmethod
    def _isDataFram(dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            print("Error: dataframe is not a Pandas DataFrame !")
            return False
        else:
            return True
