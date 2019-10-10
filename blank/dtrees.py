# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 19:28:09 2019

@author: admin
"""

#importing the library
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error,accuracy_score
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
from IPython.display import Image
import graphviz,pydotplus,pandas as pd
from sklearn import tree as clf

class classifier:
    def __init__(self,file):
        self.out=open("blank/static/output/result.txt","w")
        self.loader(file)
        self.changer()
        self.process()
        self.export()
    def loader(self,file):#To load file from directory 
        self.file=file
        self.dataset = pd.read_csv("blank/static/tmp/"+self.file)
        self.feature_cols=[i for i in (self.dataset.head(0).keys())[2:]]
        self.X = self.dataset.iloc[:, 2:].values
        self.Y = self.dataset.iloc[:, 1].values
        
    def changer(self):
        #Encoding categorical data values
        print(self.dataset.isna().sum(),file=self.out)
        self.labelencoder_Y = LabelEncoder()
        self.Y = self.labelencoder_Y.fit_transform(self.Y)
        #Splitting the dataset into the Training set and Test set
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y,test_size = 0.25, random_state = 0)
        #Feature Scaling
        self.sc = StandardScaler()
        self.X_train = self.sc.fit_transform(self.X_train)
        self.X_test = self.sc.transform(self.X_test)
    def process(self):#To make a decision tree predict
        self.classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        self.tree=self.classifier.fit(self.X_train, self.Y_train)
        self.Y_pred = self.tree.predict(self.X_test)
        #To check the accuracy
        self.err=mean_squared_error(self.Y_test, self.Y_pred)
        self.acc=accuracy_score(self.Y_test, self.Y_pred)
        print("Total Error:",round(self.err*100,2),"\nAccuracy :",round(self.acc*100,2),file=self.out)
        self.out.close()
    def export(self):#To export decision tree as a dot file  
        self.dot_data = StringIO()
        export_graphviz(self.tree, out_file=self.dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = self.feature_cols,class_names=['0','1'])
        self.graph = pydotplus.graph_from_dot_data(self.dot_data.getvalue())  
        self.graph.write_jpeg('blank/static/output/report.png')
        self.dot_data1 = clf.export_graphviz(self.tree, out_file=None)
        self.graph = graphviz.Source(self.dot_data1)
        self.graph.render('blank/static/output/result.dot')

