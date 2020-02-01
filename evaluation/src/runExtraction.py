import os
import re
import time
import glob
import re
import math


class Algo:
    truePositives = 0
    falsePositives = 0
    trueNegatives = 0
    falseNegatives = 0
    total = 0
    iteration = 0
    timeSum = 0.0

    def __init__(self, algoName, env):
        self.algoName = algoName
        self.algoWrapper = env

    def runAlgo(self, dataName, inputString, answerKey):
        maxScore = len(answerKey)
        wordCount = len(re.findall(r"\w+", inputString))
        if self.algoName == "BlankSort":
            vocab = self.algoWrapper.cleanText(inputString)
            for word in vocab:
                self.algoWrapper.loadVector(word)
        start = time.process_time()
        ranked = self.algoWrapper.rank(inputString, listSize=maxScore)
        self.timeSum += time.process_time() - start
        ranked = set(ranked)
        truePositive = len(answerKey & ranked)
        falsePositive = 0
        falseNegative = 0
        for word in ranked:
            if word not in answerKey:
                falsePositive += 1
        for word in answerKey:
            if word not in ranked:
                falseNegative += 1
        trueNegative = wordCount - truePositive - falsePositive - falseNegative
        self.truePositives += truePositive
        self.trueNegatives += trueNegative
        self.falsePositives += falsePositive
        self.falseNegatives += falseNegative
        self.total += wordCount
        self.iteration += 1
        try:
            accuracy = (self.truePositives + self.trueNegatives) / self.total
            precision = self.truePositives / (self.truePositives + self.falsePositives)
            recall = self.truePositives / (self.truePositives + self.falseNegatives)
            f1Score = 2 * (precision * recall) / (precision + recall)
            outputString = ""
            outputString += dataName + " Dataset (" + self.algoName + "):" + "\n"
            outputString += "Precision: " + str(precision) + "\n"
            outputString += "Recall: " + str(recall) + "\n"
            outputString += "F1 Score: " + str(f1Score) + "\n"
            outputString += (
                "Average Time (ms): " + str(1000 * self.timeSum / self.iteration) + "\n"
            )
            outputString += "\n"
            return outputString
        except Exception:
            return self.algoName + " - skipping output due to missing data\n\n"


def runAlgos(dataName, inputString, answerKey, algoEnvs):
    try:
        outputString = ""
        for algo in algoEnvs:
            outputString += algo.runAlgo(dataName, inputString, answerKey)
        return outputString
    except Exception:
        return "Skipping due to compatibility issues"