import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import networkx as nx
import os


class Visualization2D:
    def __init__(self):
        self.csvFile = None


    def readFile(self, fileName):
        '''data can only be read from csv file for now'''
        self.csvFile = pd.read_csv(fileName, index_col = 0)
        self.csvFile.fillna(0, inplace= True)



    def __chooseEdges(self, degree):
        allPeople = list(self.csvFile.index.values)
        edges = list()
        nodes = list()
        for i in range(0, len(allPeople)):
            addI = False
            for j in range(i + 1, len(allPeople)):
                count = 0
                for file in self.csvFile.columns.values:
                    if(self.csvFile[file][allPeople[j]] > 0 and
                            self.csvFile[file][allPeople[i]] > 0):
                        count += 1
                if count>= degree:
                    edges.append((allPeople[i], allPeople[j]))
                    if not addI:
                        nodes.append(allPeople[i])
                        addI = True
                    nodes.append(allPeople[j])
        updateNodes = list(set(nodes))
        updateNodes.sort()
        return updateNodes, edges



    def drawHeatmap(self,fileName):
        self.readFile(fileName)
        '''log the value to enhance the contrast'''
        for file in self.csvFile.columns.values:
            for person in self.csvFile.index.values:
                if self.csvFile[file][person] <= 1:
                    self.csvFile.loc[person, file] = 0.0
                else:
                    self.csvFile.loc[person, file] = \
                        math.log(self.csvFile[file][person])
        fileList = list(self.csvFile.columns.values)
        peopleList = list(self.csvFile.index.values)
        data = list()
        for file in fileList:
            temp = list()
            for people in peopleList:
                temp.append(self.csvFile[file][people])
            data.append(temp)
        print(self.csvFile)
        figure = plt.figure();
        ax = figure.add_subplot(111)
        ax.set_yticks(range(len(fileList)))
        ax.set_yticklabels(fileList)
        ax.set_xticks(range(len(peopleList)))
        ax.set_xticklabels(peopleList)

        im = ax.imshow(data, cmap=plt.cm.gray_r)

        plt.xticks(rotation = 90)
        plt.colorbar(im)

        title = fileName.split('.')[0].split('/')[-1]
        plt.title(title)
        plt.show()


    def drawCoreNetWork(self, fileName):
        self.readFile(fileName)
        print("please input the weigh of edges:")
        degree = int(input())
        print("drawing core notwork...")
        NETuple = self.__chooseEdges(degree)
        nodes = list(NETuple[0])
        edges = list(NETuple[1])
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        nx.draw(G,with_labels=True)
        print("succeed!")
        plt.show()


    def drawOverviewNetWork(self, fileName):
        self.readFile(fileName)
        print("please input the weigh of edges:")
        degree = int(input())
        print("drawing overview network...")
        NETuple = self.__chooseEdges(degree)
        nodes = list(NETuple[0])
        edges = list(NETuple[1])

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        nx.draw(G, node_color = 'r', edge_color = 'b', node_size = 30)
        print("succeed!")
        plt.show()



v =Visualization2D()
#v.drawHeatmap('Data/testData.csv')
v.drawHeatmap('Data/alluxio-20h50w.csv')
v.drawCoreNetWork('Data/alluxio-20h50w.csv')
v.drawOverviewNetWork('Data/alluxio.csv')






