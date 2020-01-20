import os
import re
import time


class Algo:
    truePositives = 0
    falsePositives = 0
    trueNegatives = 0
    falseNegatives = 0
    total = 0
    iteration = 0
    timeSum = 0.0

    def __init__(self, algoName, dataName):
        self.algoName = algoName
        self.dataName = dataName

    def runAlgo(self, inputString, answerKey, algoWrapper, allPaths):
        maxScore = len(answerKey)
        wordCount = len(re.findall(r"\w+", inputString))
        start = time.process_time()
        ranked = algoWrapper.rank(inputString, listSize=maxScore)
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
        accuracy = (self.truePositives + self.trueNegatives) / self.total
        precision = self.truePositives / (self.truePositives + self.falsePositives)
        recall = self.truePositives / (self.truePositives + self.falseNegatives)
        f1Score = 2 * (precision * recall) / (precision + recall)
        self.iteration += 1
        print(self.dataName + " Dataset (" + self.algoName + "):")
        print("Iteration:", self.iteration, "/", len(allPaths))
        # print("Accuracy:",accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1Score)
        print("Average Time (ms):", 1000 * self.timeSum / self.iteration)
        print()
