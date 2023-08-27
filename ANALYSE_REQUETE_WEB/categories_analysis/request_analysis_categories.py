#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 14:55:36 2022

@author: Jocelyn GIROD
Classe d'analyse par catégorie de la requête.
"""

from common_core.request_analysis import RequestAnalysis
from report.pdfreport import PdfReport


class RequestAnalysisCategories(RequestAnalysis):
    keyNormalStr = "NORMAL"
    keySlowStr = "SLOW"
    keyVerySlowStr = "VERY_SLOW"
    keyErrorStr = "ERROR"

    nbRequestsNormal = 0
    nbRequestsSlow = 0
    nbRequestsVerySlow = 0
    nbRequestsError = 0

    countByCategorieArray = RequestAnalysis.npy.empty(4, dtype=int)
    percentageByCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)

    meanNormalCategory = 0.0
    meanSlowCategory = 0.0
    meanVerySlowCategory = 0.0
    meanErrorCategory = 0.0
    standardDeviationNormalCategory = 0.0
    standardDeviationSlowCategory = 0.0
    standardDeviationVerySlowCategory = 0.0
    standardDeviationErrorCategory = 0.0

    minMaxNormalCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)
    minMaxSlowCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)
    minMaxVerySlowCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)
    minMaxErrorCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)

    quantileNormalCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)
    quantileSlowCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)
    quantileVerySlowCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)
    quantileErrorCategoryArray = RequestAnalysis.npy.empty(4, dtype=float)

    medianNormalCategory = 0.0
    medianSlowCategory = 0.0
    medianVerySlowCategory = 0.0
    medianErrorCategory = 0.0

    highFrequencyNormalArray = []
    highFrequencySlowArray = []
    highFrequencyVerySlowArray = []
    highFrequencyErrorArray = []

    """Récupère le nombre de requêtes par catégorie.
    :returns: un tableau contenant le décompte par cétégorie.
        index 0 : normal
        index 1 : slow
        index 2 : very slow
        index 3 : error
    :rtype: un tableau d'entiers
    """

    def getCountByCategorie(self):

        countByCategoryArray = self.npy.empty(4, dtype=int)
        numNormal = (self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == 'NORMAL').sum()
        numSlow = (self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == 'SLOW').sum()
        numVerySlow = (self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == 'VERY_SLOW').sum()
        numError = (self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == 'ERROR').sum()

        countByCategoryArray[0] = numNormal
        countByCategoryArray[1] = numSlow
        countByCategoryArray[2] = numVerySlow
        countByCategoryArray[3] = numError

        return countByCategoryArray

    """Récupère ce que représente en pourcentage les requêtes par catégorie.
    :returns: un tableau contenant les pourcentages:
        index 0 : normal
        index 1 : slow
        index 2 : very slow
        index 3 : error
    :rtype: un tableau de float
    """

    def getPercentageByCategories(self):

        percentageByCategoryArray = self.npy.empty(4, dtype=float)
        countByCategoryArray = self.getCountByCategorie()

        # Normal
        percentageNormal = (countByCategoryArray[0] * 100) / self.nbRequest
        percentageByCategoryArray[0] = round(percentageNormal, self.floatAccuracy)
        # Slow
        percentageSlow = (countByCategoryArray[1] * 100) / self.nbRequest
        percentageByCategoryArray[1] = round(percentageSlow, self.floatAccuracy)
        # Very slow
        percentageVerySlow = (countByCategoryArray[2] * 100) / self.nbRequest
        percentageByCategoryArray[2] = round(percentageVerySlow, self.floatAccuracy)
        # Error
        percentageError = (countByCategoryArray[3] * 100) / self.nbRequest
        percentageByCategoryArray[3] = round(percentageError, self.floatAccuracy)

        return percentageByCategoryArray

    """Récupère le temps moyen d'une requête pour la catégorie.
    :param categoryName: le nom de la catégorie.
    :type categoryName: une string.
    :return: la moyenne.
    :rtype: un float.
    """

    def getMeanForCategory(self, categoryName):

        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return self.getMean(self.request_helper.COLUMN_EXEC_TIME, categoryDataFrame)

    """Récupère l'écart type de la catégorie.
    :param categoryName: lle nom de la catégorie.
    :type categoryName: une string.
    :return: la moyenne.
    :rtype: un float.
    """

    def getStandardDeviationForCategory(self, categoryName):

        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return self.getStandardDeviation(self.request_helper.COLUMN_EXEC_TIME, categoryDataFrame)

    """Récupère la valeur min et max de la catégorie.
    :param categoryName: le nom de la catégorie.
    :type categoryName: une string.
    :returns: un tableau contenant le min (indexe 0) et le max (indexe 1).
    :rtype: array
    """

    def getMinMaxValuesForCategory(self, categoryName):

        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return self.getMinMaxValues(self.request_helper.COLUMN_EXEC_TIME, categoryDataFrame)

    """Récupère le premier et le troisième quartile de la catégorie.
    :param categoryName: le nom de la catégorie.
    :type categoryName: une string.
    :returns: un tableau contenant le premier quartile (indexe 0) et le troisième quartile (indexe 1).
    :rtype: array
    """

    def getQuantileQ1Q3ForCategory(self, categoryName):

        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return self.getQuantileQ1Q3(self.request_helper.COLUMN_EXEC_TIME, categoryDataFrame)

    """Récupère la médiane de la catégorie.
    :param categoryName: le nom de la categorie.
    :type categoryName: une string.
    :returns: la médiane.
    :rtype: un float.
    """

    def getMedianForCategory(self, categoryName):

        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return self.getMedian(self.request_helper.COLUMN_EXEC_TIME, categoryDataFrame)

    """Retourne la valeur qui a la plus haute fréquence dans la série passée en pramètre.
    :param categoryName: le nom de la categorie.
    :type categoryName: une string.
    :returns: un tableau contenant le couple nombre de répétitions (indexe 0), valeur (index 1).
    :rtype: une tableau. 
    """

    def getHighFrequencyByCategory(self, categoryName):

        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return self.getHighFrequency(self.request_helper.COLUMN_EXEC_TIME, categoryDataFrame)

    """Récupère le nombre de requêtes par catégorie.
    :param categoryName: le nom de la categorie.
    :type categoryName: une string.
    :returns: le nombre de requêtes pour la catégorie.
    :rtype: un int.
    """
    def getNbRequestsByCategory(self, categoryName):
        if type(categoryName) is not str:
            print("Error: categoryName is not a str !")
            return
        else:
            categoryDataFrame = self.requestDataframe[
                self.requestDataframe[self.request_helper.COLUMN_USER_EXPERIENCE] == categoryName]
            return categoryDataFrame[self.request_helper.COLUMN_EXEC_TIME].count()

    """Lance l'analyse du dataframe et imprime le résultat dans un pdf ou la console ou les deux.
    :param pdfObject: le pdf.
    :type pdfObject: un FPDF.
    :param isReport: indique si l'on veut ou non imprimer le résultat de l'analyse dans un pdf. Par défaut la valeur est True.
    :type isReport: booléen.
    :param isConsol: indique si l'on veut ou non imprimer le résultat de l'analyse dans la console. Par défaut la valeur est False.
    :type isConsol: booléen.
    """

    def analyze(self, pdfObject, isReport=True, isConsol=False):

        if not self._isDataFram(self.requestDataframe):
            return

        self.countByCategorieArray = self.getCountByCategorie()
        self.percentageByCategoryArray = self.getPercentageByCategories()

        self.meanNormalCategory = self.getMeanForCategory(self.keyNormalStr)
        self.meanSlowCategory = self.getMeanForCategory(self.keySlowStr)
        self.meanVerySlowCategory = self.getMeanForCategory(self.keyVerySlowStr)
        self.meanErrorCategory = self.getMeanForCategory(self.keyErrorStr)

        self.standardDeviationNormalCategory = self.getStandardDeviationForCategory(self.keyNormalStr)
        self.standardDeviationSlowCategory = self.getStandardDeviationForCategory(self.keySlowStr)
        self.standardDeviationVerySlowCategory = self.getStandardDeviationForCategory(self.keyVerySlowStr)
        self.standardDeviationErrorCategory = self.getStandardDeviationForCategory(self.keyErrorStr)

        self.minMaxNormalCategoryArray = self.getMinMaxValuesForCategory(self.keyNormalStr)
        self.minMaxSlowCategoryArray = self.getMinMaxValuesForCategory(self.keySlowStr)
        self.minMaxVerySlowCategoryArray = self.getMinMaxValuesForCategory(self.keyVerySlowStr)
        self.minMaxErrorCategoryArray = self.getMinMaxValuesForCategory(self.keyErrorStr)

        self.quantileNormalCategoryArray = self.getQuantileQ1Q3ForCategory(self.keyNormalStr)
        self.quantileSlowCategoryArray = self.getQuantileQ1Q3ForCategory(self.keySlowStr)
        self.quantileVerySlowCategoryArray = self.getQuantileQ1Q3ForCategory(self.keyVerySlowStr)
        self.quantileErrorCategoryArray = self.getQuantileQ1Q3ForCategory(self.keyErrorStr)

        self.medianNormalCategory = self.getMeanForCategory(self.keyNormalStr)
        self.medianSlowCategory = self.getMeanForCategory(self.keySlowStr)
        self.medianVerySlowCategory = self.getMeanForCategory(self.keyVerySlowStr)
        self.medianErrorCategory = self.getMeanForCategory(self.keyErrorStr)

        self.highFrequencyNormalArray = self.getHighFrequencyByCategory(self.keyNormalStr)
        self.highFrequencySlowArray = self.getHighFrequencyByCategory(self.keySlowStr)
        self.highFrequencyVerySlowArray = self.getHighFrequencyByCategory(self.keyVerySlowStr)
        self.highFrequencyErrorArray = self.getHighFrequencyByCategory(self.keyErrorStr)

        self.nbRequestsNormal = self.getNbRequestsByCategory(self.keyNormalStr)
        self.nbRequestsSlow = self.getNbRequestsByCategory(self.keySlowStr)
        self.nbRequestsVerySlow = self.getNbRequestsByCategory(self.keyVerySlowStr)
        self.nbRequestsError = self.getNbRequestsByCategory(self.keyErrorStr)

        if isReport:
            self.__createReportInPdf(pdfObject)

        if isConsol:
            self.__diplayReportInConsol()

    """Créé le diagramme circulaire pour les catégories"""

    def __createPieChartForCategories(self, pdfObject: object):

        if not isinstance(pdfObject, PdfReport):
            return

        # Taille des portions
        normalSize = round(self.percentageByCategoryArray[0] * 1.8, 2)
        slowSize = round(self.percentageByCategoryArray[1] * 1.8, 2)
        verySlowSize = round(self.percentageByCategoryArray[2] * 1.8, 2)
        errorSize = round(self.percentageByCategoryArray[3] * 1.8, 2)

        labels = ["NORMAL", "SLOW", "VERY_SLOW", "ERROR"]
        colors = ['cornflowerblue', 'forestgreen', 'orange', 'red']
        sizes = [normalSize, slowSize, verySlowSize, errorSize]
        explode = (0.3, 0, 0, 0)  # on sépare la catégorie NORMAL

        fig1, ax1 = self.matPlt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90, wedgeprops={'linewidth': 3}, textprops={'fontweight': 'bold'})

        chartPath = self.rootPicturePath + 'CategoriesPieChart.png'
        self.matPlt.savefig(chartPath)
        pdfObject.addPicture(chartPath, 640 / 5.5, 480 / 5.5)

    """Imprime le rapport dans un fichier pdf.
    :param pdfObject: le pdf.
    :type pdfObject: un FPDF.
    """

    def __createReportInPdf(self, pdfObject: object):

        if not isinstance(pdfObject, PdfReport):
            return

        # Titre
        pdfObject.addSubTitle("Analyse par catégories", self.request_helper.GREEN_RGB[0],
                              self.request_helper.GREEN_RGB[1],
                              self.request_helper.GREEN_RGB[2])

        # Nombre de requêtes par catégorie
        nbNormalText = "Nombre de requêtes NORMAL: " + str(self.countByCategorieArray[0]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[0]) + " %)."
        pdfObject.addText(nbNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        nbSlowText = "Nombre de requêtes SLOW: " + str(self.countByCategorieArray[1]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[1]) + " %)."
        pdfObject.addText(nbSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        nbVerySlowText = "Nombre de requêtes VERY_SLOW: " + str(self.countByCategorieArray[2]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[2]) + " %)."
        pdfObject.addText(nbVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        nbErrorText = "Nombre de requêtes ERROR: " + str(self.countByCategorieArray[3]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[3]) + " %)."
        pdfObject.addText(nbErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        pdfObject.ln(4)
        self.__createPieChartForCategories(pdfObject)
        pdfObject.ln(4)

        pdfObject.add_page()
        # Catégorie NORMAL *******************************
        self.__createReportInPdfForNormalCategory(pdfObject)
        # Catégorie SLOW *********************************
        self.__createReportInPdfForSlowCategory(pdfObject)
        # Catégorie VERY SLOW ****************************
        self.__createReportInPdfForVerySlowCategory(pdfObject)
        # Catégorie ERROR ********************************
        self.__createReportInPdfForErrorCategory(pdfObject)

    """Imprime le résultat de l'analyse dans la console"""

    def __diplayReportInConsol(self):

        print("Analyse par catégories")
        print("")
        nbNormalStr = "Nombre de requêtes NORMAL: " + str(self.countByCategorieArray[0]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[0]) + " %)."
        print(nbNormalStr)
        nbSlowText = "Nombre de requêtes SLOW: " + str(self.countByCategorieArray[1]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[1]) + " %)."
        print(nbSlowText)
        nbVerySlowText = "Nombre de requêtes VERY_SLOW: " + str(self.countByCategorieArray[2]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[2]) + " %)."
        print(nbVerySlowText)
        nbErrorText = "Nombre de requêtes ERROR: " + str(self.countByCategorieArray[3]) + " sur " + str(
            self.nbRequest) + " (soit " + str(self.percentageByCategoryArray[3]) + " %)."
        print(nbErrorText)
        print("")

        # Requêtes NORMAL
        print("Requêtes NORMAL ------------------------------------")
        print("")

        # Moyenne
        meanNormalText = "Le temps moyen est: " + str(self.meanNormalCategory) + " ms."
        print(meanNormalText)

        # Min et Max
        minNormalText = "Valeur MIN: " + str(self.minMaxNormalCategoryArray[0]) + " ms."
        maxNormalText = "Valeur MAX: " + str(self.minMaxNormalCategoryArray[1]) + " ms."
        print(minNormalText)
        print(maxNormalText)

        # Etendue
        extentNormal = self.minMaxNormalCategoryArray[1] - self.minMaxNormalCategoryArray[0]
        extentNormalText = "L'étendue est de: " + str(extentNormal) + " ms."
        print(extentNormalText)

        # Ecart-type
        standardDeviationNormalText = "L'écart-type est de: " + str(self.standardDeviationNormalCategory) + " ms."
        print(standardDeviationNormalText)
        print("")

        # Quartile Q1 (25%) et Q3 (75%)
        # Q1
        print("Premier quartile: ")
        q1_25NormalText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileNormalCategoryArray[0]) + " ms."
        print(q1_25NormalText)
        q1_75NormalText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileNormalCategoryArray[0]) + " ms."
        print(q1_75NormalText)
        print("")
        # Q3
        print("Troisième quartile: ")
        q3_75NormalText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileNormalCategoryArray[1]) + " ms."
        print(q3_75NormalText)
        q3_25NormalText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileNormalCategoryArray[1]) + " ms."
        print(q3_25NormalText)
        print("")

        # Intervalle
        intervalNormalText = "L'intervalle [" + str(self.quantileNormalCategoryArray[0]) + " ms ; " + str(
            self.quantileNormalCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        print(intervalNormalText)
        print("")

        # Mediane
        medianNormalText = "Valeur de la médiane: " + str(self.medianNormalCategory) + " ms."
        print(medianNormalText)
        medianLower50NormalText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianNormalCategory) + " ms."
        print(medianLower50NormalText)
        medianSuperior50NormalText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianNormalCategory) + " ms."
        print(medianSuperior50NormalText)
        print("")

        # Plus haute fréquence:
        if self.highFrequencyNormalArray[0] > 0:
            frequencyNormalStr = "( f = " + str(self.highFrequencyNormalArray[0]) + "/" + str(self.nbRequestsNormal) + " )."
            highFrequencyNormalStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencyNormalArray[1]) + " ms " + frequencyNormalStr
            print(highFrequencyNormalStr)
        else:
            frequencyNormalStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsNormal) + " )."
            print(frequencyNormalStr)
        print("")

        # Requêtes SLOW
        print("Requêtes SLOW ----------------------------------------")
        print("")

        # Moyenne
        meanSlowText = "Le temps moyen est: " + str(self.meanSlowCategory) + " ms."
        print(meanSlowText)

        # Min et Max
        minSlowText = "Valeur MIN: " + str(self.minMaxSlowCategoryArray[0]) + " ms."
        maxSlowText = "Valeur MAX: " + str(self.minMaxSlowCategoryArray[1]) + " ms."
        print(minSlowText)
        print(maxSlowText)

        # Etendue
        extentSlow = self.minMaxSlowCategoryArray[1] - self.minMaxSlowCategoryArray[0]
        extentSlowText = "L'étendue est de: " + str(extentSlow) + " ms."
        print(extentSlowText)

        # Ecart-type
        standardDeviationSlowText = "L'écart-type est de: " + str(self.standardDeviationSlowCategory) + " ms."
        print(standardDeviationSlowText)
        print("")

        # Quartile Q1 (25%) et Q3 (75%)
        # Q1
        print("Premier quartile: ")
        q1_25SlowText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileSlowCategoryArray[0]) + " ms."
        print(q1_25SlowText)
        q1_75SlowText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileSlowCategoryArray[0]) + " ms."
        print(q1_75SlowText)
        print("")
        # Q3
        print("Troisième quartile: ")
        q3_75SlowText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileSlowCategoryArray[1]) + " ms."
        print(q3_75SlowText)
        q3_25SlowText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileSlowCategoryArray[1]) + " ms."
        print(q3_25SlowText)
        print("")

        # Intervalle
        intervalSlowText = "L'intervalle [" + str(self.quantileSlowCategoryArray[0]) + " ms ; " + str(
            self.quantileSlowCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        print(intervalSlowText)
        print("")

        # Mediane
        medianSlowText = "Valeur de la médiane: " + str(self.medianSlowCategory) + " ms."
        print(medianSlowText)
        medianLower50SlowText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianSlowCategory) + " ms."
        print(medianLower50SlowText)
        medianSuperior50SlowText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianSlowCategory) + " ms."
        print(medianSuperior50SlowText)
        print("")

        # Plus haute fréquence:
        if self.highFrequencySlowArray[0] > 0:
            frequencySlowStr = "( f = " + str(self.highFrequencySlowArray[0]) + "/" + str(
                self.nbRequestsSlow) + " )."
            highFrequencySlowStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencySlowArray[1]) + " ms " + frequencySlowStr
            print(highFrequencySlowStr)
        else:
            frequencySlowStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsSlow) + " )."
            print(frequencySlowStr)
        print("")

        # Requêtes VERY_SLOW
        print("Requêtes VERY_SLOW -----------------------------------")
        print("")

        # Moyenne
        meanVerySlowText = "Le temps moyen est: " + str(self.meanVerySlowCategory) + " ms."
        print(meanVerySlowText)

        # Min et Max
        minVerySlowText = "Valeur MIN: " + str(self.minMaxVerySlowCategoryArray[0]) + " ms."
        maxVerySlowText = "Valeur MAX: " + str(self.minMaxVerySlowCategoryArray[1]) + " ms."
        print(minVerySlowText)
        print(maxVerySlowText)

        # Etendue
        extentVerySlow = self.minMaxVerySlowCategoryArray[1] - self.minMaxVerySlowCategoryArray[0]
        extentVerySlowText = "L'étendue est de: " + str(extentVerySlow) + " ms."
        print(extentVerySlowText)

        # Ecart-type
        standardDeviationVerySlowText = "L'écart-type est de: " + str(self.standardDeviationVerySlowCategory) + " ms."
        print(standardDeviationVerySlowText)
        print("")

        # Quartile Q1 (25%) et Q3 (75%)
        # Q1
        print("Premier quartile: ")
        q1_25VerySlowText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[0]) + " ms."
        print(q1_25VerySlowText)
        q1_75VerySlowText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[0]) + " ms."
        print(q1_75VerySlowText)
        print("")
        # Q3
        print("Troisième quartile: ")
        q3_75VerySlowText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[1]) + " ms."
        print(q3_75VerySlowText)
        q3_25VerySlowText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[1]) + " ms."
        print(q3_25VerySlowText)
        print("")

        # Intervalle
        intervalVerySlowText = "L'intervalle [" + str(self.quantileVerySlowCategoryArray[0]) + " ms ; " + str(
            self.quantileVerySlowCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        print(intervalVerySlowText)
        print("")

        # Mediane
        medianVerySlowText = "Valeur de la médiane: " + str(self.medianVerySlowCategory) + " ms."
        print(medianVerySlowText)
        medianLower50VerySlowText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianVerySlowCategory) + " ms."
        print(medianLower50VerySlowText)
        medianSuperior50VerySlowText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianVerySlowCategory) + " ms."
        print(medianSuperior50VerySlowText)
        print("")

        # Plus haute fréquence:
        if self.highFrequencyVerySlowArray[0] > 0:
            frequencyVerySlowStr = "( f = " + str(self.highFrequencyVerySlowArray[0]) + "/" + str(
                self.nbRequestsVerySlow) + " )."
            highFrequencyVerySlowStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencyVerySlowArray[1]) + " ms " + frequencyVerySlowStr
            print(highFrequencyVerySlowStr)
        else:
            frequencyVerySlowStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsVerySlow) + " )."
            print(frequencyVerySlowStr)
        print("")

        # Requêtes ERROR
        print("Requêtes ERROR ---------------------------------------")
        print("")

        # Moyenne
        meanErrorText = "Le temps moyen est: " + str(self.meanErrorCategory) + " ms."
        print(meanErrorText)

        # Min et Max
        minErrorText = "Valeur MIN: " + str(self.minMaxErrorCategoryArray[0]) + " ms."
        maxErrorText = "Valeur MAX: " + str(self.minMaxErrorCategoryArray[1]) + " ms."
        print(minErrorText)
        print(maxErrorText)

        # Etendue
        extentError = self.minMaxErrorCategoryArray[1] - self.minMaxErrorCategoryArray[0]
        extentErrorText = "L'étendue est de: " + str(extentError) + " ms."
        print(extentErrorText)

        # Ecart-type
        standardDeviationErrorText = "L'écart-type est de: " + str(
            self.standardDeviationErrorCategory) + " ms."
        print(standardDeviationErrorText)
        print("")

        # Quartile Q1 (25%) et Q3 (75%)
        # Q1
        print("Premier quartile: ")
        q1_25ErrorText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileErrorCategoryArray[0]) + " ms."
        print(q1_25ErrorText)
        q1_75ErrorText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileErrorCategoryArray[0]) + " ms."
        print(q1_75ErrorText)
        print("")
        # Q3
        print("Troisième quartile: ")
        q3_75ErrorText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileErrorCategoryArray[1]) + " ms."
        print(q3_75ErrorText)
        q3_25ErrorText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileErrorCategoryArray[1]) + " ms."
        print(q3_25ErrorText)
        print("")

        # Intervalle
        intervalErrorText = "L'intervalle [" + str(self.quantileErrorCategoryArray[0]) + " ms ; " + str(
            self.quantileErrorCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        print(intervalErrorText)
        print("")

        # Mediane
        medianErrorText = "Valeur de la médiane: " + str(self.medianErrorCategory) + " ms."
        print(medianErrorText)
        medianLower50ErrorText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianErrorCategory) + " ms."
        print(medianLower50ErrorText)
        medianSuperior50ErrorText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianErrorCategory) + " ms."
        print(medianSuperior50ErrorText)
        print("")

        # Plus haute fréquence:
        if self.highFrequencyErrorArray[0] > 0:
            frequencyErrorStr = "( f = " + str(self.highFrequencyErrorArray[0]) + "/" + str(
                self.nbRequestsError) + " )."
            highFrequencyErrorStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencyErrorArray[1]) + " ms " + frequencyErrorStr
            print(highFrequencyErrorStr)
        else:
            frequencyErrorStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsError) + " )."
            print(frequencyErrorStr)

    """Créé le raport pdf pour la catégorie NORMAL"""

    def __createReportInPdfForNormalCategory(self, pdfObject: object):

        if not isinstance(pdfObject, PdfReport):
            return

        # Catégorie NORMAL *******************************
        pdfObject.addSubTitleUnderlinne("Requêtes NORMAL", self.request_helper.BLUE_LIGHT_RGB[0],
                                        self.request_helper.BLUE_LIGHT_RGB[1],
                                        self.request_helper.BLUE_LIGHT_RGB[2])
        pdfObject.ln(1)

        # Moyenne
        meanNormalText = "Le temps moyen est: " + str(self.meanNormalCategory) + " ms."
        pdfObject.addText(meanNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        # Min et Max
        minNormalText = "Valeur MIN: " + str(self.minMaxNormalCategoryArray[0]) + " ms."
        maxNormalText = "Valeur MAX: " + str(self.minMaxNormalCategoryArray[1]) + " ms."
        pdfObject.addText(minNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.addText(maxNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Etendue
        extentNormal = self.minMaxNormalCategoryArray[1] - self.minMaxNormalCategoryArray[0]
        extentNormalText = "L'étendue est de: " + str(extentNormal) + " ms."
        pdfObject.addText(extentNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Ecart-type
        standardDeviationNormalText = "L'écart-type est de: " + str(self.standardDeviationNormalCategory) + " ms."
        pdfObject.addText(standardDeviationNormalText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(1)

        # Quartile Q1 (25%) et Q3 (75%)

        # Q1
        pdfObject.addText("Premier quartile: ", self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_25NormalText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileNormalCategoryArray[0]) + " ms."
        pdfObject.addText(q1_25NormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_75NormalText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileNormalCategoryArray[0]) + " ms."
        pdfObject.addText(q1_75NormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Q3
        pdfObject.addText("Troisième quartile: ", self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_75NormalText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileNormalCategoryArray[1]) + " ms."
        pdfObject.addText(q3_75NormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_25NormalText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileNormalCategoryArray[1]) + " ms."
        pdfObject.addText(q3_25NormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Intervalle
        intervalNormalText = "L'intervalle [" + str(self.quantileNormalCategoryArray[0]) + " ms ; " + str(
            self.quantileNormalCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        pdfObject.addText(intervalNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Médiane
        medianNormalText = "Valeur de la médiane: " + str(self.medianNormalCategory) + " ms."
        pdfObject.addText(medianNormalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianLower50NormalText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianNormalCategory) + " ms."
        pdfObject.addText(medianLower50NormalText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianSuperior50NormalText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianNormalCategory) + " ms."
        pdfObject.addText(medianSuperior50NormalText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        pdfObject.ln(2)

        # Plus haute fréquence:
        if self.highFrequencyNormalArray[0] > 0:
            frequencyNormalStr = "( f = " + str(self.highFrequencyNormalArray[0]) + "/" + str(self.nbRequestsNormal) + " )."
            highFrequencyNormalStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencyNormalArray[1]) + " ms " + frequencyNormalStr
            pdfObject.addText(highFrequencyNormalStr, self.request_helper.BLACK_RGB[0],
                              self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])
        else:
            frequencyNormalStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsNormal) + " )."
            pdfObject.addText(frequencyNormalStr, self.request_helper.BLACK_RGB[0],
                              self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])

        pdfObject.ln(5)

    """Créé le raport pdf pour la catégorie SLOW"""

    def __createReportInPdfForSlowCategory(self, pdfObject: object):

        if not isinstance(pdfObject, PdfReport):
            return

        # Catégorie SLOW *******************************
        pdfObject.addSubTitleUnderlinne("Requêtes SLOW", self.request_helper.BLUE_LIGHT_RGB[0],
                                        self.request_helper.BLUE_LIGHT_RGB[1],
                                        self.request_helper.BLUE_LIGHT_RGB[2])
        pdfObject.ln(1)

        # Moyenne
        meanSlowText = "Le temps moyen est: " + str(self.meanSlowCategory) + " ms."
        pdfObject.addText(meanSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        # Min et Max
        minSlowText = "Valeur MIN: " + str(self.minMaxSlowCategoryArray[0]) + " ms."
        maxSlowText = "Valeur MAX: " + str(self.minMaxSlowCategoryArray[1]) + " ms."
        pdfObject.addText(minSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.addText(maxSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Etendue
        extentSlow = self.minMaxSlowCategoryArray[1] - self.minMaxSlowCategoryArray[0]
        extentSlowText = "L'étendue est de: " + str(extentSlow) + " ms."
        pdfObject.addText(extentSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Ecart-type
        standardDeviationSlowText = "L'écart-type est de: " + str(self.standardDeviationSlowCategory) + " ms."
        pdfObject.addText(standardDeviationSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(1)

        # Quartile Q1 (25%) et Q3 (75%)

        # Q1
        pdfObject.addText("Premier quartile: ", self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_25SlowText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileSlowCategoryArray[0]) + " ms."
        pdfObject.addText(q1_25SlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_75SlowText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileSlowCategoryArray[0]) + " ms."
        pdfObject.addText(q1_75SlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Q3
        pdfObject.addText("Troisième quartile: ", self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_75SlowText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileSlowCategoryArray[1]) + " ms."
        pdfObject.addText(q3_75SlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_25SlowText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileSlowCategoryArray[1]) + " ms."
        pdfObject.addText(q3_25SlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Intervalle
        intervalSlowText = "L'intervalle [" + str(self.quantileSlowCategoryArray[0]) + " ms ; " + str(
            self.quantileSlowCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        pdfObject.addText(intervalSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Médiane
        medianSlowText = "Valeur de la médiane: " + str(self.medianSlowCategory) + " ms."
        pdfObject.addText(medianSlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianLower50SlowText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianSlowCategory) + " ms."
        pdfObject.addText(medianLower50SlowText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianSuperior50SlowText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianSlowCategory) + " ms."
        pdfObject.addText(medianSuperior50SlowText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Plus haute fréquence:
        if self.highFrequencySlowArray[0] > 0:
            frequencySlowStr = "( f = " + str(self.highFrequencySlowArray[0]) + "/" + str(self.nbRequestsSlow) + " )."
            highFrequencySlowStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencySlowArray[1]) + " ms " + frequencySlowStr
            pdfObject.addText(highFrequencySlowStr, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])
        else:
            frequencySlowStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsSlow) + " )."
            pdfObject.addText(frequencySlowStr, self.request_helper.BLACK_RGB[0],
                              self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])

        pdfObject.ln(5)

    """Créé le raport pdf pour la catégorie VERY SLOW"""

    def __createReportInPdfForVerySlowCategory(self, pdfObject: object):
        if not isinstance(pdfObject, PdfReport):
            return

        # Catégorie VERY SLOW *******************************
        pdfObject.addSubTitleUnderlinne("Requêtes VERY_SLOW", self.request_helper.BLUE_LIGHT_RGB[0],
                                        self.request_helper.BLUE_LIGHT_RGB[1],
                                        self.request_helper.BLUE_LIGHT_RGB[2])
        pdfObject.ln(1)

        # Moyenne
        meanVerySlowText = "Le temps moyen est: " + str(self.meanVerySlowCategory) + " ms."
        pdfObject.addText(meanVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        # Min et Max
        minVerySlowText = "Valeur MIN: " + str(self.minMaxVerySlowCategoryArray[0]) + " ms."
        maxVerySlowText = "Valeur MAX: " + str(self.minMaxVerySlowCategoryArray[1]) + " ms."
        pdfObject.addText(minVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.addText(maxVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Etendue
        extentVerySlow = self.minMaxVerySlowCategoryArray[1] - self.minMaxVerySlowCategoryArray[0]
        extentVerySlowText = "L'étendue est de: " + str(extentVerySlow) + " ms."
        pdfObject.addText(extentVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Ecart-type
        standardDeviationVerySlowText = "L'écart-type est de: " + str(self.standardDeviationVerySlowCategory) + " ms."
        pdfObject.addText(standardDeviationVerySlowText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(1)

        # Quartile Q1 (25%) et Q3 (75%)

        # Q1
        pdfObject.addText("Premier quartile: ", self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_25VerySlowText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[0]) + " ms."
        pdfObject.addText(q1_25VerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_75VerySlowText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[0]) + " ms."
        pdfObject.addText(q1_75VerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(10)

        # Q3
        pdfObject.addText("Troisième quartile: ", self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_75VerySlowText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[1]) + " ms."
        pdfObject.addText(q3_75VerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_25VerySlowText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileVerySlowCategoryArray[1]) + " ms."
        pdfObject.addText(q3_25VerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Intervalle
        intervalVerySlowText = "L'intervalle [" + str(self.quantileVerySlowCategoryArray[0]) + " ms ; " + str(
            self.quantileVerySlowCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        pdfObject.addText(intervalVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Médiane
        medianVerySlowText = "Valeur de la médiane: " + str(self.medianVerySlowCategory) + " ms."
        pdfObject.addText(medianVerySlowText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianLower50VerySlowText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianVerySlowCategory) + " ms."
        pdfObject.addText(medianLower50VerySlowText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianSuperior50VerySlowText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianVerySlowCategory) + " ms."
        pdfObject.addText(medianSuperior50VerySlowText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Plus haute fréquence:
        if self.highFrequencyVerySlowArray[0] > 0:
            frequencyVerySlowStr = "( f = " + str(self.highFrequencyVerySlowArray[0]) + "/" + str(
                self.nbRequestsVerySlow) + " )."
            highFrequencyVerySlowStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencyVerySlowArray[1]) + " ms " + frequencyVerySlowStr
            pdfObject.addText(highFrequencyVerySlowStr, self.request_helper.BLACK_RGB[0],
                              self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])
        else:
            frequencyVerySlowStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsVerySlow) + " )."
            pdfObject.addText(frequencyVerySlowStr, self.request_helper.BLACK_RGB[0],
                              self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])

        pdfObject.ln(5)

    """Créé le raport pdf pour la catégorie ERROR"""

    def __createReportInPdfForErrorCategory(self, pdfObject: object):
        if not isinstance(pdfObject, PdfReport):
            return

        # Catégorie ERROR *******************************
        pdfObject.addSubTitleUnderlinne("Requêtes ERROR", self.request_helper.BLUE_LIGHT_RGB[0],
                                        self.request_helper.BLUE_LIGHT_RGB[1],
                                        self.request_helper.BLUE_LIGHT_RGB[2])
        pdfObject.ln(1)

        # Moyenne
        meanErrorText = "Le temps moyen est: " + str(self.meanErrorCategory) + " ms."
        pdfObject.addText(meanErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        # Min et Max
        minErrorText = "Valeur MIN: " + str(self.minMaxErrorCategoryArray[0]) + " ms."
        maxErrorText = "Valeur MAX: " + str(self.minMaxErrorCategoryArray[1]) + " ms."
        pdfObject.addText(minErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.addText(maxErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Etendue
        extentError = self.minMaxErrorCategoryArray[1] - self.minMaxErrorCategoryArray[0]
        extentErrorText = "L'étendue est de: " + str(extentError) + " ms."
        pdfObject.addText(extentErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Ecart-type
        standardDeviationErrorText = "L'écart-type est de: " + str(self.standardDeviationErrorCategory) + " ms."
        pdfObject.addText(standardDeviationErrorText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(1)

        # Quartile Q1 (25%) et Q3 (75%)

        # Q1
        pdfObject.addText("Premier quartile: ", self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_25ErrorText = "25% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileErrorCategoryArray[0]) + " ms."
        pdfObject.addText(q1_25ErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_75ErrorText = "75% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileErrorCategoryArray[0]) + " ms."
        pdfObject.addText(q1_75ErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Q3
        pdfObject.addText("Troisième quartile: ", self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_75ErrorText = "75% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.quantileErrorCategoryArray[1]) + " ms."
        pdfObject.addText(q3_75ErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_25ErrorText = "25% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.quantileErrorCategoryArray[1]) + " ms."
        pdfObject.addText(q3_25ErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Intervalle
        intervalErrorText = "L'intervalle [" + str(self.quantileErrorCategoryArray[0]) + " ms ; " + str(
            self.quantileErrorCategoryArray[1]) + " ms] contient 50% des mesures du temps d'exécution."
        pdfObject.addText(intervalErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Médiane
        medianErrorText = "Valeur de la médiane: " + str(self.medianErrorCategory) + " ms."
        pdfObject.addText(medianErrorText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianLower50ErrorText = "50% des mesures du temps d'exécution sont inférieures ou égales à: " + str(
            self.medianErrorCategory) + " ms."
        pdfObject.addText(medianLower50ErrorText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianSuperior50ErrorText = "50% des mesures du temps d'exécution sont supérieures ou égales à: " + str(
            self.medianErrorCategory) + " ms."
        pdfObject.addText(medianSuperior50ErrorText, self.request_helper.BLACK_RGB[0],
                          self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Plus haute fréquence:
        if self.highFrequencyErrorArray[0] > 0:
            frequencyErrorStr = "( f = " + str(self.highFrequencyErrorArray[0]) + "/" + str(self.nbRequestsError) + " )."
            highFrequencyErrorStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
                self.highFrequencyErrorArray[1]) + " ms " + frequencyErrorStr
            pdfObject.addText(highFrequencyErrorStr, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])
        else:
            frequencyErrorStr = "Toutes les mesures n'apparaissent qu'une seule fois (fréquence = 1/" + str(
                self.nbRequestsError) + " )."
            pdfObject.addText(frequencyErrorStr, self.request_helper.BLACK_RGB[0],
                              self.request_helper.BLACK_RGB[1],
                              self.request_helper.BLACK_RGB[2])

        pdfObject.ln(5)
