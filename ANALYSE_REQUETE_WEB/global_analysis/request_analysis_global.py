#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 13:41:03 2022

@author: Jocelyn GIROD
Classe d'analyse globale de la requête.
"""

from common_core.request_analysis import RequestAnalysis
from report.pdfreport import PdfReport
import scipy.stats


class RequestAnalysisGlobal(RequestAnalysis):
    """Lance l'analyse du dataframe et imprime le résultat dans un pdf ou la console ou les deux.
    :param: pdfObject: le pdf.
    :type: pdfObject: un FPDF.
    :param:isReport: indique si l'on veut ou non imprimer le résultat de l'analyse dans un pdf. Par défaut la valeur est True.
    :type: isReport: booléen.
    :param: isConsol: indique si l'on veut ou non imprimer le résultat de l'analyse dans la console. Par défaut la valeur est False.
    :type: isConsol: booléen.
    """

    def analyze(self, pdfObject, isReport=True, isConsol=False):

        if not self._isDataFram(self.requestDataframe):
            return

        self.meanExecTimeTotalRequest = self.getMean(self.request_helper.COLUMN_EXEC_TIME, self.requestDataframe)
        self.minMaxArray = self.getMinMaxValues(self.request_helper.COLUMN_EXEC_TIME, self.requestDataframe)
        self.standardDeviation = self.getStandardDeviation(self.request_helper.COLUMN_EXEC_TIME, self.requestDataframe)
        self.quantileArray = self.getQuantileQ1Q3(self.request_helper.COLUMN_EXEC_TIME, self.requestDataframe)
        self.median = self.getMedian(self.request_helper.COLUMN_EXEC_TIME, self.requestDataframe)
        self.highFrequencyArray = self.getHighFrequency(self.request_helper.COLUMN_EXEC_TIME, self.requestDataframe)
        self.meanMinusStandardDeviation = round(self.meanExecTimeTotalRequest - self.standardDeviation, self.floatAccuracy)
        self.meanPlusStandardDeviation = round(self.meanExecTimeTotalRequest + self.standardDeviation, self.floatAccuracy)

        self.threshold = self.meanPlusStandardDeviation * self.edge

        if isReport:
            self.__createReportInPdf(pdfObject)

        if isConsol:
            self.__diplayReportInConsol()

    """Création du diagrame de Gausse suivant la loi Normale"""

    def __createNormalGaussChart(self, pdfObject: object, x_min, x_max, chartname):

        if not isinstance(pdfObject, PdfReport):
            return

        # comme espacement on prend l'écart-type
        space = int(self.standardDeviation)
        x = self.npy.linspace(x_min, x_max, space)
        y = scipy.stats.norm.pdf(x, self.meanExecTimeTotalRequest, self.standardDeviation)

        # affichage pour:
        # a = moyenne - écart-type, b = moyenne + écart-type
        # P(a<= X <= b)
        px = self.npy.linspace(self.meanMinusStandardDeviation, self.meanPlusStandardDeviation, space)
        py = scipy.stats.norm.pdf(px, self.meanExecTimeTotalRequest, self.standardDeviation)

        # affichage pour:
        # edge correspond à une marge de sécurité
        # a1 = (moyenne - écart-type) * 1,5, b1 = (moyenne + écart-type)
        # P(a1<= X <= b1)
        px_1 = self.npy.linspace(-self.threshold, self.threshold, space)
        py_1 = scipy.stats.norm.pdf(px_1, self.meanExecTimeTotalRequest, self.standardDeviation)

        color_grey_light = '#868b8f'
        color_blue = '#12609e'
        color_blue_light = '#6b9bc2'
        color_orange = '#ecb223'

        # Mean
        mean_legend = 'moyenne (' + str(self.meanExecTimeTotalRequest) + ' ms)'
        self.matPlt.plot([self.meanExecTimeTotalRequest, self.meanExecTimeTotalRequest], [0.0, scipy.stats.norm.pdf(
            self.meanExecTimeTotalRequest, self.meanExecTimeTotalRequest, self.standardDeviation)], color=color_orange,
                         label=mean_legend, linestyle='--', linewidth=1.2)
        # Full
        self.matPlt.plot(x, y, color='black')
        self.matPlt.fill_between(x, y, color=color_grey_light, alpha=1.0)

        # (mean + std) * edge
        edge_legend = 'seuil (' + str(self.threshold) + ' ms)'
        self.matPlt.plot([self.threshold, self.threshold],
                         [0.0, scipy.stats.norm.pdf(self.threshold, self.meanExecTimeTotalRequest, self.standardDeviation)],
                         color='red', label=edge_legend)
        self.matPlt.fill_between(px_1, py_1, color=color_blue_light, alpha=1.0)

        # mean + std / mean - std
        self.matPlt.plot([self.meanMinusStandardDeviation, self.meanMinusStandardDeviation], [0.0, scipy.stats.norm.pdf(
            self.meanMinusStandardDeviation, self.meanExecTimeTotalRequest, self.standardDeviation)], color='black')
        self.matPlt.plot([self.meanPlusStandardDeviation, self.meanPlusStandardDeviation], [0.0, scipy.stats.norm.pdf(
            self.meanPlusStandardDeviation, self.meanExecTimeTotalRequest, self.standardDeviation)], color='black')
        # astuce pour avoir la légende de la couleur bleue - on trace une ligne bleue dans l'intervalle px/py de la couleur bleue
        meanStd_legend = '[moyenne - écart-type;moyenne + écart-type]'

        self.matPlt.plot([self.meanMinusStandardDeviation + 1000, self.meanMinusStandardDeviation + 1000], [0.0, 0.000001],
                         color=color_blue,
                         label=meanStd_legend)
        self.matPlt.fill_between(px, py, color=color_blue, alpha=1.0)
        self.matPlt.grid(True, linewidth=1)

        self.matPlt.xlim(x_min, x_max)
        self.matPlt.ylim(0, 0.000175)

        self.matPlt.title('Distribution Normale du temps d\'exécution des requêtes (courbe de Gauss)', fontsize=10)
        self.matPlt.xlabel('Temps d\'exécution en ms')
        self.matPlt.ylabel('Distribution Normale')

        self.matPlt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), ncol=1)

        chartPath = self.rootPicturePath + chartname
        self.matPlt.savefig(chartPath, bbox_inches='tight', dpi=100)
        pdfObject.addPicture(chartPath, 982 / 5, 453 / 5)

        self.matPlt.figure().clear(True)

    """Calcul la probabilité que la variable aléatoire a une valeur inférieur ou égale a une certaine valeur
    :param: value: la valeur.
    :type: value: un float.
    :param: mean: la moyenne.
    :type: mean: un float.
    :param: std: l'écart-type.
    :type: std: un float.
    :returns: la probabilité.
    :rtype: un float.
    """

    @staticmethod
    def __probNormalLessThanOrEqual(value, mean, std):
        return scipy.stats.norm.cdf(value, mean, std)

    """Calcul la probabilité que la variable aléatoire a une valeur supérieur ou égale a une certaine valeur
        :param: value: la valeur.
        :type: value: un float.
        :param: mean: la moyenne.
        :type: mean: un float.
        :param: std: l'écart-type.
        :type: std: un float.
        :returns: la probabilité.
        :rtype: un float.
        """

    @staticmethod
    def __probNormalGreaterThanOrEqual(value, mean, std):
        return scipy.stats.norm.sf(value, mean, std)

    """Imprime le rapport dans un fichier pdf.
    :param: pdfObject: le pdf.
    :type: pdfObject: un FPDF.
    """

    def __createReportInPdf(self, pdfObject: object):

        if not isinstance(pdfObject, PdfReport):
            return

        # Titre
        pdfObject.addSubTitle("Analyse globale", self.request_helper.GREEN_RGB[0], self.request_helper.GREEN_RGB[1],
                              self.request_helper.GREEN_RGB[2])

        # Moyenne
        meanText = "Le temps moyen d'exécution d'une requête est: " + str(self.meanExecTimeTotalRequest) + " ms."
        pdfObject.addText(meanText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Etendue
        minValueText = "Valeur MIN: " + str(self.minMaxArray[0]) + " ms."
        maxValueText = "Valeur MAX: " + str(self.minMaxArray[1]) + " ms."
        pdfObject.addText(minValueText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.addText(maxValueText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        extent = self.minMaxArray[1] - self.minMaxArray[0]
        extentText = "L'étendue de la série des mesures du temps d'exécution est: " + str(extent) + " ms."
        pdfObject.addText(extentText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Ecart-type
        standDeviationText = "L'écart type de la série des mesures du temps d'exécution d'une requête est de: " + str(
            self.standardDeviation) + " ms."
        pdfObject.addText(standDeviationText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Quartile Q1 (25%) et Q3 (75%)

        # Q1
        pdfObject.addText("Premier quartile: ", self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_25Text = "25% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(
            self.quantileArray[0]) + " ms."
        pdfObject.addText(q1_25Text, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q1_75Text = "75% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(
            self.quantileArray[0]) + " ms."
        pdfObject.addText(q1_75Text, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)
        # Q3
        pdfObject.addText("Troisième quartile: ", self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_75Text = "75% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(
            self.quantileArray[1]) + " ms."
        pdfObject.addText(q3_75Text, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        q3_25Text = "25% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(
            self.quantileArray[1]) + " ms."
        pdfObject.addText(q3_25Text, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Intervalle
        intervalText = "L'intervalle [" + str(self.quantileArray[0]) + " ms ; " + str(
            self.quantileArray[1]) + " ms] contient 50% des mesures du temps d'exécution de la requête."
        pdfObject.addText(intervalText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(2)

        # Médiane
        medianText = "Valeur de la médiane: " + str(self.median) + " ms."
        pdfObject.addText(medianText, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianLower50Text = "50% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(
            self.median) + " ms."
        pdfObject.addText(medianLower50Text, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        medianSuperior50Text = "50% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(
            self.median) + " ms."
        pdfObject.addText(medianSuperior50Text, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        pdfObject.ln(2)

        # Plus haute fréquence:
        frequencyStr = "( f = " + str(self.highFrequencyArray[0]) + "/" + str(self.nbRequest) + " )."
        highFrequencyStr = "La mesure ayant la plus haute fréquence de répétition est: " + str(
            self.highFrequencyArray[1]) + " ms " + frequencyStr
        pdfObject.addText(highFrequencyStr, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(5)

        # Courbes de Gausse
        normalChartText = "Courbe de Gauss (distribution Normale):"
        pdfObject.ln(2)
        pdfObject.addText(normalChartText, self.request_helper.BLUE_RGB[0], self.request_helper.BLUE_RGB[1],
                          self.request_helper.BLUE_RGB[2], True, 'B')
        x_min = (self.minMaxArray[1] * -1)
        x_max = self.minMaxArray[1]
        chartName = 'normal_distribution.png'
        self.__createNormalGaussChart(pdfObject, x_min, x_max, chartName)

        x_min_zoom = -6000
        x_max_zoom = 11500
        chartName = 'normal_distribution_zoom.png'
        self.__createNormalGaussChart(pdfObject, x_min_zoom, x_max_zoom, chartName)
        pdfObject.ln(2)

        intervalleMeanStdStr = "[moyenne - écart-type ; moyenne + écart-type] = [" + str(self.meanMinusStandardDeviation) + " ms ; " + str(self.meanPlusStandardDeviation) + " ms]."
        pdfObject.addText(intervalleMeanStdStr, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2], True, '', 8)
        pdfObject.ln(5)

        # Probabilité que la variable aléatoire P(mean-std <= X <= mean + std)
        p1 = self.__probNormalLessThanOrEqual(self.meanMinusStandardDeviation, self.meanExecTimeTotalRequest, self.standardDeviation)
        p2 = self.__probNormalGreaterThanOrEqual(self.meanPlusStandardDeviation, self.meanExecTimeTotalRequest, self.standardDeviation)
        pX = 1 - (p1 + p2)
        pXIntervalle = "La probabilité que le temps d'exécution d'une requête soit dans l'intervalle [" + str(
            self.meanMinusStandardDeviation) + " ms; " + str(self.meanPlusStandardDeviation) + " ms] est de: "
        pdfObject.addText(pXIntervalle, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pXStr = str(round(pX, self.floatAccuracy)) + " soit " + str(round(pX, self.floatAccuracy) * 100) + "%."
        pdfObject.addText(pXStr, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        pdfObject.ln(3)

        # Probabilité que la variable aléatoire soit supérieur ou égale au seuil
        p3 = self.__probNormalGreaterThanOrEqual(self.threshold, self.meanExecTimeTotalRequest, self.standardDeviation)
        p3Str = "La probabilité que le temps d'exécution d'une requête soit supérieur au seuil de " + str(self.threshold) + " ms est de:"
        pdfObject.addText(p3Str, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        p3Str = str(round(p3, self.floatAccuracy)) + " soit " + str(round(p3, self.floatAccuracy) * 100) + "%."
        pdfObject.addText(p3Str, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        # Probabilité que la variable aléatoire soit inféroeur ou égale au seuil
        p4 = 1 - p3
        p4Str = "La probabilité que le temps d'exécution d'une requête soit inférieur au seuil de " + str(self.threshold) + " ms est de:"
        pdfObject.addText(p4Str, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])
        p4Str = str(round(p4, self.floatAccuracy)) + " soit " + str(round(p4, self.floatAccuracy) * 100) + "%."
        pdfObject.addText(p4Str, self.request_helper.BLACK_RGB[0], self.request_helper.BLACK_RGB[1],
                          self.request_helper.BLACK_RGB[2])

        pdfObject.ln(5)

    """Imprime le résultat de l'analyse dans la console"""

    def __diplayReportInConsol(self):

        # Moyenne
        print("Le temps moyen d'exécution d'une requête est: " + str(self.meanExecTimeTotalRequest) + " ms.")
        print("")

        # Etendue
        print("Valeur MIN: " + str(self.minMaxArray[0]) + " ms.")
        print("Valeur MAX: " + str(self.minMaxArray[1]) + " ms.")

        extent = self.minMaxArray[1] - self.minMaxArray[0]
        extentText = "L'étendue de la série des mesures du temps d'exécution est: " + str(extent) + " ms."
        print(extentText)
        print("")

        # Ecart-type
        print("L'écart type de la série des mesures du temps d'exécution d'une requête est de: " + str(
            self.standardDeviation) + " ms.")
        print("")

        # Quartile Q1 (25%) et Q3 (75%)

        # Q1
        print("Premier quartile:")
        print("25% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(
            self.quantileArray[0]) + " ms.")
        print("75% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(
            self.quantileArray[0]) + " ms.")
        print("")
        # Q3
        print("Troisième quartile:")
        print("75% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(
            self.quantileArray[1]) + " ms.")
        print("25% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(
            self.quantileArray[1]) + " ms.")
        print("")
        # Intervalle
        print("L'intervalle [" + str(self.quantileArray[0]) + " ms ; " + str(
            self.quantileArray[1]) + " ms] contient 50% des mesures du temps d'exécution de la requête.")
        print("")

        # Médiane
        print("Valeur de la médiane: " + str(self.median) + " ms.")
        print("50% des mesures du temps d'exécution de la requête sont inférieures ou égales à: " + str(
            self.median) + " ms.")
        print("50% des mesures du temps d'exécution de la requête sont supérieures ou égales à: " + str(
            self.median) + " ms.")
