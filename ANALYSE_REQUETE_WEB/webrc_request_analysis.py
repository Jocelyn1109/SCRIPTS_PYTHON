#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 12:40:11 2022

@author: Jocelyn GIROD
Script principal pour l'analyse des requêtes Webrc.
"""
import sys

# Ajout du répertoire Common dans le système de fichier
# pour l'import de Util et PdfReport
# NOTE: remplacer mon_compte par la vraie valeur
sys.path.append('/home/mon_compte/DEV/Python/Common/')

import pandas as pd
from report.pdfreport import PdfReport
from util.util import Util
from helper.request_helper import RequestHelper
from util.datetime_util import DateTimeUtil
from global_analysis.request_analysis_global import RequestAnalysisGlobal
from categories_analysis.request_analysis_categories import RequestAnalysisCategories

pdf = PdfReport(unit='mm')
request_helper = RequestHelper()
datetime_util = DateTimeUtil()
util = Util()

# PDF
pdf.add_page()

# Lecture du fichier csv, remplacement des valeurs NNan et affichage des indormations du dataframe
# request_dataframe = pd.read_csv("data/Export.csv", sep=",", header=None)
# request_dataframe = pd.read_csv("data/Export_26864_8jours.csv", sep=",", header=None)
request_dataframe = pd.read_csv("data/Export_4.csv", sep=",", header=None)
# Remplacement des valeurs NaN dans le dataframe
request_dataframe = Util.replaceNaNValues(request_dataframe, "Unknown")
util.dataFrameInfos(request_dataframe)

# Suppression des 7 premières lignes du dataframe et reset des indexes
request_dataframe = Util.deleteRows(request_dataframe, [0, 1, 2, 3, 4, 5, 6])
request_dataframe.reset_index(drop=True, inplace=True)

# Définition du header
request_dataframe = Util.defineHeader(request_dataframe, 0, 1)

# Récupération du nom de la transaction
# Ligne 1 et colonne Business Transaction
transaction_name = request_dataframe.loc[1, request_helper.COLUMN_BUSINESS_TRANSACTION]
print("")
text_transaction_studied = "Informations sur la transaction étudiée: "
print("Transaction étudiée: " + transaction_name)
pdf.addTitle("Etude de transaction web".upper(), 125, 125, 125)
pdf.addChapterTitle(text_transaction_studied, request_helper.BLACK_RGB[0], request_helper.BLACK_RGB[1],
                    request_helper.BLACK_RGB[2])
pdf.addText("Nom de la transaction: ", request_helper.BLACK_RGB[0], request_helper.BLACK_RGB[1],
            request_helper.BLACK_RGB[2], False)
pdf.addText(transaction_name, request_helper.BLUE_RGB[0], request_helper.BLUE_RGB[1], request_helper.BLUE_RGB[2])

# Taille de l'échantillon étudié
nbRequests = Util.getNumberLinesInTable(request_dataframe)
print("Taille de l'échantillon (nombre de requêtes): " + str(nbRequests))
print("")
sample_size_text = "Taille de l'échantillon (nombre de requêtes): " + str(nbRequests)
pdf.addText(sample_size_text, request_helper.BLACK_RGB[0], request_helper.BLACK_RGB[1], request_helper.BLACK_RGB[2])

# Suppression des colonnes inutilisées ou qui ne sont plus utiles
columns_to_delete = [request_helper.COLUMN_LATENCY, request_helper.COLUMN_URL,
                     request_helper.COLUMN_BUSINESS_TRANSACTION, request_helper.COLUMN_TIER, request_helper.COLUMN_NODE,
                     request_helper.COLUMN_ARCHIVED]
Util.deleteColumns(request_dataframe, columns_to_delete)

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
pdf.addText("Intervalle d'étude de l'échantillon: " + study_range + ".", request_helper.BLACK_RGB[0],
            request_helper.BLACK_RGB[1], request_helper.BLACK_RGB[2])

studyLengthInSec = datetime_util.getDurationInSecondBetweenTwoDates(minDate, maxDate, '%d-%m-%Y %H:%M:%S')

hh_mm_ss_str = datetime_util.getTimeDDHHMMSS(studyLengthInSec)
print("Durée de l'étude: " + str(hh_mm_ss_str))
print("")
pdf.addText("Durée de l'étude: " + str(hh_mm_ss_str) + ".", request_helper.BLACK_RGB[0], request_helper.BLACK_RGB[1],
            request_helper.BLACK_RGB[2])
pdf.ln(5)

print("Start analysis...")
print("")
# ANALYSE GLOBALE
request_analysis_global = RequestAnalysisGlobal(request_dataframe, nbRequests)
request_analysis_global.analyze(pdf, True, True)
print("")

# ANALYSE PAR GATEGORIE
request_analysis_by_category = RequestAnalysisCategories(request_dataframe, nbRequests)
request_analysis_by_category.analyze(pdf, True, True)
print("")
print("End analysis !")
print("")

# Ecriture du fichier pdf.
print("Création du rapport PDF.")
pdf.output("report/analyse_report.pdf")
