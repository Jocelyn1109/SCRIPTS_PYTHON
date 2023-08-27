#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 18:09:16 2022

@author: Jocelyn GIROD
"""
import sys

# Ajout du répertoire Common dans le système de fichier
# pour l'import de Util
# NOTE: remplacer mon_compte par la vraie valeur
sys.path.append( '/home/mon_compte/DEV/Python/Common/' )

import pandas as pd
from util.util import Util
from report.pdfreport import PdfReport
from util.datetime_util import DateTimeUtil
from request_helper import RequestHelper
from request_analysis_global import RequestAnalysisGlobal


# Couleurs
BLACK_RGB = (0,0,0)
BLUE_RGB = (14,65,215)

util = Util()
datetime_util = DateTimeUtil()
request_helper = RequestHelper()
pdf = PdfReport(unit='mm')


# Lecture du fichier csv dans un dataframe
request_dataframe = pd.read_csv("DATA/Export.csv", sep=",", header=None)
# Remplacement des valeurs NaN dans le dataframe
request_dataframe = util.replaceNaNValues(request_dataframe,"Unknown")
util.dataFrameInfos(request_dataframe)

# Suppression des 7 premières lignes du dataframe et reset des indexes
request_dataframe = util.deleteRows(request_dataframe, [0,1,2,3,4,5,6])
request_dataframe.reset_index(drop=True, inplace=True)


# Définition du header
request_dataframe = util.defineHeader(request_dataframe, 0, 1)

# PDF
pdf.add_page()
pdf.drawFrame()

# Récupération du nom de la transaction
# Ligne 1 et colonne Business Transaction
transaction_name = request_dataframe.loc[1,request_helper.COLUMN_BUSINESS_TRANSACTION]
print("")
text_transaction_studied = "Informations sur transaction étudiée: "
print("Transaction étudiée: " + transaction_name)
pdf.addTitle("Etude de transaction web".upper(),125, 125, 125)
pdf.addChapterTitle(text_transaction_studied,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
pdf.addText("Nom de la transaction: ",BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2],False)
pdf.addText(transaction_name,BLUE_RGB[0],BLUE_RGB[1],BLUE_RGB[2])


# Taille de l'échantillon étudié
nbRequests = util.getNumberLinesInTable(request_dataframe)
print("Taille de l'échantillon: " + str(nbRequests))
print("")
size_text = "Taille de l'échantillon (nombre de requêtes): " + str(nbRequests)
pdf.addText(size_text,BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])

# Suppression des colonnes inutilisées ou qui ne sont plus utiles
columns_to_delete = [request_helper.COLUMN_LATENCY,request_helper.COLUMN_URL,request_helper.COLUMN_BUSINESS_TRANSACTION,request_helper.COLUMN_TIER,request_helper.COLUMN_NODE,request_helper.COLUMN_ARCHIVED]
util.deleteColumns(request_dataframe, columns_to_delete)

# Récupération de la colonne Time
timeColumn = request_dataframe[request_helper.COLUMN_TIME]
# Conversion de la colonne Time au format datetime
timeColumn = pd.to_datetime(timeColumn)
# Conversiion de la colonne Exe Time au format float
request_dataframe[request_helper.COLUMN_EXEC_TIME] = request_dataframe[request_helper.COLUMN_EXEC_TIME].astype(float)

timeColumn = timeColumn.dt.strftime('%d-%m-%Y %H:%M:%S')
minDate = min(timeColumn)
maxDate = max(timeColumn)
study_range = '[' + str(minDate) + ' ; ' + str(maxDate) + ']'
print("Intervalle d'étude de l'échantillon: " + study_range)
pdf.addText("Intervalle d'étude de l'échantillon: " + study_range + ".",BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])

studyLengthInSec = datetime_util.getDurationInSecondBetweenTwoDates(minDate, maxDate, '%d-%m-%Y %H:%M:%S')

hh_mm_ss_str = datetime_util.getTimeDDHHMMSS(studyLengthInSec)
print("Durée de l'étude: " + str(hh_mm_ss_str))
print("")



# ANALYSE GLOBALE
request_analysis_global = RequestAnalysisGlobal(request_dataframe)
pdf.ln(4)
pdf.addChapterTitle("Analyse globale",BLACK_RGB[0],BLACK_RGB[1],BLACK_RGB[2])
request_analysis_global.analyze(pdf)

# Moyenne
meanExecTimeTotalRequest = request_dataframe[request_helper.COLUMN_EXEC_TIME].mean()

# Etendue
print("Valeur MAX: " + str(request_dataframe[request_helper.COLUMN_EXEC_TIME].max()) + " ms.")
print("Valeur MIN: " + str(request_dataframe[request_helper.COLUMN_EXEC_TIME].min()) + " ms.")
print("")
extent = request_dataframe[request_helper.COLUMN_EXEC_TIME].max() - request_dataframe[request_helper.COLUMN_EXEC_TIME].min()

# Ecart type
standardDeviation = request_dataframe[request_helper.COLUMN_EXEC_TIME].std()

print("Le temps moyen d'exécution d'une requête est: " + str(meanExecTimeTotalRequest) + " ms")
print("")
print("L'étendue de la série des mesures du temps d'exécution d'une requête est de: " + str(extent) + " ms.")
print("")
print("L'écart type de la série des mesures du temps d'exécution d'une requête est de: " + str(standardDeviation) + " ms.")
print("")


# Premier quartile de la série
q1 = request_dataframe[request_helper.COLUMN_EXEC_TIME].quantile(0.25)
print("Premier quartile.")
print("25% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(q1) + " ms.")
print("75% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(q1) + " ms.")
print("")
# Troisième quartile
q3 = request_dataframe[request_helper.COLUMN_EXEC_TIME].quantile(0.75)
print("Troisième quartile.")
print("75% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(q3) + " ms.")
print("25% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(q3) + " ms.")
print("")
print("L'intervalle [" + str(q1) + ";" + str(q3) + "] contient 50% des mesures du temps d'exécution de la requête.")
print("")
# Mediane
med = request_dataframe[request_helper.COLUMN_EXEC_TIME].median()
print("Valeur de la médiane: " + str(med) + " ms.")
print("50% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(med) + " ms.")
print("50% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(med) + " ms.")
print("")


# CATEGORIES

numSlow = (request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == 'SLOW').sum()
numVerySlow = (request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == 'VERY_SLOW').sum()
numError = (request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == 'ERROR').sum()
numNormal = (request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == 'NORMAL').sum()

percentageSlow = (numSlow * 100)/nbRequests
percentageVerySlow = (numVerySlow * 100)/nbRequests
percentageError = (numError * 100)/nbRequests
percentageNormal = (numNormal *100)/nbRequests

print("Nombre de requêtes SLOW: " + str(numSlow) + " sur " + str(nbRequests) + " (soit " + str(percentageSlow) + " %)")
print("Nombre de requêtes VERY_SLOW: " + str(numVerySlow) + " sur " + str(nbRequests) + " (soit " + str(percentageVerySlow) + " %)")
print("Nombre de requêtes ERROR: " + str(numError) + " sur " + str(nbRequests) + " (soit " + str(percentageError) + " %)")
print("Nombre de requêtes NORMAL: " + str(numNormal) + " sur " + str(nbRequests) + " (soit " + str(percentageNormal) + " %)")
print("")

valuesExecTimeSlowRequest = request_dataframe[request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == "SLOW"][request_helper.COLUMN_EXEC_TIME]
valuesExecTimeVerySlowRequest = request_dataframe[request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == "VERY_SLOW"][request_helper.COLUMN_EXEC_TIME]
valuesExecTimeErrorRequest = request_dataframe[request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == "ERROR"][request_helper.COLUMN_EXEC_TIME]
valuesExecTimeNormalRequest = request_dataframe[request_dataframe[request_helper.COLUMN_USER_EXPERIENCE] == "NORMAL"][request_helper.COLUMN_EXEC_TIME]

meanExecTimeSlowRequest = valuesExecTimeSlowRequest.astype(float).mean()
meanExecTimeVerySlowRequest = valuesExecTimeVerySlowRequest.astype(float).mean()
meanExecTimeErrorRequest = valuesExecTimeErrorRequest.astype(float).mean()
meanExecTimeNormalRequest = valuesExecTimeNormalRequest.astype(float).mean()
print("Le temps moyen d'exécution d'une requête SLOW est: " + str(meanExecTimeSlowRequest) + " ms")
print("Le temps moyen d'exécution d'une requête VERY_SLOW est: " + str(meanExecTimeVerySlowRequest) + " ms")
print("Le temps moyen d'exécution d'une requête ERROR est: " + str(meanExecTimeErrorRequest) + " ms")
print("Le temps moyen d'exécution d'une requête NORMALE est: " + str(meanExecTimeNormalRequest) + " ms")
print("")


execTimeColumnData = util.getAllDataFromColumn(request_dataframe, request_helper.COLUMN_EXEC_TIME, False)
dictionaryRepeatedValues = request_helper.extractRepeatedValue(execTimeColumnData)

print("")
frequencies_dataframe = request_dataframe[request_helper.COLUMN_EXEC_TIME].value_counts()
print("")
#frequencies_dataframe[request_helper.COLUMN_EXEC_TIME] = frequencies_dataframe[request_helper.COLUMN_EXEC_TIME].astype(float)
#print(frequencies_dataframe[frequencies_dataframe[request_helper.COLUMN_EXEC_TIME]])
print(frequencies_dataframe)


#print(dictionaryRepeatedValues)
#print("")
# résumé statistique de la série
print("Résumé des statistiques de la série:")
print(request_dataframe.describe())
print("")
print("Création du rapport PDF.")
pdf.output('analyse_report.pdf','F')
    
