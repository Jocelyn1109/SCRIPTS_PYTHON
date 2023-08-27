#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 19:22:46 2022

@author: Jocelyn GIROD
Analyse globale des données de la transaction
"""

import pandas as pd
from request_helper import RequestHelper
from fpdf import FPDF
import numpy as np

class RequestAnalysisGlobal:
    
    # Couleurs
    BLACK_RGB = (0,0,0)
    BLUE_RGB = (14,65,215)
    
    requestDataframe = None
    request_helper = RequestHelper()
    meanExecTimeTotalRequest = 0.0
    standardDeviation = 0.0
    minMaxArray = np.empty(2,dtype=float)
    quantileArray = np.empty(2,dtype=float)
    median = 0.0
    
    
    def __init__(self, dataframe):
        
        if not self.__isDataFram(dataframe):
            return
        
        self.requestDataframe = dataframe
    
    
    """Récupère la moyenne des données d'une colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :returns: la moyenne.
    :rtype: float.
    """
    def getMean(self, columnName):
        
        if type(columnName) is not str:
            print ("Error: columnName is not a str !")
            return
        else:
            # Conversion de la colonne au format float
            self.requestDataframe[columnName] = self.requestDataframe[columnName].astype(float)
            # Calcul de la moyenne
            return self.requestDataframe[columnName].mean()
    
    
    
    """Récupère l'écart type des valeurs de la colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :returns: l'écart type.
    :rtype: float.
    """
    def getStandardDeviation(self,columnName):
        
        if type(columnName) is not str:
            print ("Error: columnName is not a str !")
            return
        else:
            return self.requestDataframe[columnName].std()
        
    
    """Récupère la valeur min et max d'une colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :returns: un tableau contenant le min (indexe 0) et le max (indexe 1).
    :rtype: array
    """
    def getMinMaxValues(self,columnName):
        
        minMaxArray = np.empty(2,dtype=float)
        if type(columnName) is not str:
            print ("Error: columnName is not a str !")
            return
        else:
            minValue = self.requestDataframe[columnName].min()
            maxValue = self.requestDataframe[columnName].max()
            minMaxArray[0] = minValue
            minMaxArray[1] = maxValue
        
        return minMaxArray
        
    
    """Récupère le premier et le troisième quartile de la colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :returns: un tableau contenant le premier quartile (indexe 0) et le troisième quartile (indexe 1).
    :rtype: array
    """
    def getQuantileQ1Q3(self,columnName):
        
        quantileArray = np.empty(2,dtype=float)
        if type(columnName) is not str:
            print ("Error: columnName is not a str !")
            return
        else:
            # Premier quartile de la série
            q1 = self.requestDataframe[columnName].quantile(0.25)
            # Trooisième quartile de la série
            q3 = self.requestDataframe[columnName].quantile(0.75)
            quantileArray[0] = q1
            quantileArray[1] = q3
        
        return quantileArray
    
    
    """Récupère la médiane de la colonne.
    :param columnName: le nom de la colonne.
    :type columnName: une string.
    :returns: la médiane.
    :rtype: un float.
    """
    def getMedian(self,columnName):
        
        if type(columnName) is not str:
            print ("Error: columnName is not a str !")
            return
        else:
            return self.requestDataframe[columnName].median()
            
    
    
    """Lance l'analyse du dataframe et imprime le résultat dans un pdf ou la console ou les deux.
    :param pdfObject: le pdf.
    :type pdfObject: un FPDF.
    :param isReport: indique si l'on veut ou non imprimer le résultat de l'analyse dans un pdf. Par défaut la valeur est True.
    :type isReport: booléen.
    :param isConsol: indique si l'on veut ou non imprimer le résultat de l'analyse dans la console. Par défaut la valeur est False.
    :type isConsol: booléen.
    """
    def analyze(self, pdfObject, isReport=True, isConsol=False):
        
        if not self.__isDataFram(self.requestDataframe):
            return
        
        self.meanExecTimeTotalRequest = self.getMean(self.request_helper.COLUMN_EXEC_TIME)
        self.minMaxArray = self.getMinMaxValues(self.request_helper.COLUMN_EXEC_TIME)
        self.standardDeviation = self.getStandardDeviation(self.request_helper.COLUMN_EXEC_TIME)
        self.quantileArray = self.getQuantileQ1Q3(self.request_helper.COLUMN_EXEC_TIME)
        self.median = self.getMedian(self.request_helper.COLUMN_EXEC_TIME)
        
        
        if isReport == True:
            self.__createReportInPdf(pdfObject)
    
    
    
    """Imprime le rapport dans un fichier pdf.
    :param pdfObject: le pdf.
    :type pdfObject: un FPDF.
    """
    def __createReportInPdf(self,pdfObject):
        
        if not isinstance(pdfObject, FPDF):
            return
            
        # Moyenne
        meanText = "Le temps moyen d'exécution d'une requête est: " + str(self.meanExecTimeTotalRequest) + " ms."
        pdfObject.addText(meanText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        
        # Etendue
        minValueText = "Valeur MIN: " + str(self.minMaxArray[0]) + " ms."
        maxValueText = "Valeur MAX: " + str(self.minMaxArray[1]) + " ms."
        pdfObject.addText(minValueText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.addText(maxValueText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        
        extent = self.minMaxArray[1] - self.minMaxArray[0]
        extentText = "L'étendue de la série des mesures du temps d'exécution est: " + str(extent) + " ms."
        pdfObject.addText(extentText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        
        # Ecart-type
        standDeviationText = "L'écart type de la série des mesures du temps d'exécution d'une requête est de: " + str(self.standardDeviation) + " ms."
        pdfObject.addText(standDeviationText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        
        # Quartile Q1 (25%) et Q3 (75%)
    
        # Q1
        pdfObject.addText("Premier quartile: ",self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        q1_25Text = "25% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(self.quantileArray[0]) + " ms."
        pdfObject.addText(q1_25Text,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        q1_75Text = "75% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(self.quantileArray[0]) + " ms."
        pdfObject.addText(q1_75Text,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        # Q3
        pdfObject.addText("Troisième quartile: ",self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        q3_75Text = "75% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(self.quantileArray[1]) + " ms."
        pdfObject.addText(q3_75Text,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        q3_25Text = "25% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(self.quantileArray[1]) + " ms."
        pdfObject.addText(q3_25Text,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        # Intervalle
        intervalText = "L'intervalle [" + str(self.quantileArray[0]) + ";" + str(self.quantileArray[1]) + "] contient 50% des mesures du temps d'exécution de la requête."
        pdfObject.addText(intervalText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        pdfObject.ln(2)
        
        # Médiane
        medianText = "Valeur de la médiane: " + str(self.median) + " ms."
        pdfObject.addText(medianText,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        medianLower50Text = "50% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(self.median) + " ms."
        pdfObject.addText(medianLower50Text,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        medianSuperior50Text = "50% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(self.median) + " ms."
        pdfObject.addText(medianSuperior50Text,self.BLACK_RGB[0],self.BLACK_RGB[1],self.BLACK_RGB[2])
        
      
        
        

    """Valide si ou ou non la variable datafram est un dataFrame Pandas.
    :param dataframe: le dataframe à vérifier.
    :type dataframe: un dataframe Panda.
    :returns: True si c'est un DataFrame sinon False
    :rtype: booléen
    """
    def __isDataFram(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            print("Error: dataframe is not a Pandas DataFrame !")
            return False
        else:
            return True
    

        

