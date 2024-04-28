'''
-------------------------
---       main        ---
-------------------------

'''
# Import libs and Classes
from Bibs import pd, np, sys, mysql, os
from Classes import Data, TestData, IdealFunctions, DB_Handling

# Init-Paths and Files
testFile    = r'\test.csv'              # Using Raw-String => r'\'
trainFile   = r'\train.csv'
fcnsFile    = r'\ideal.csv'

codePath    = os.getcwd()
projectPath = os.path.dirname(codePath)
dataPath    = projectPath + r'\DataSet'         

# Create Data-Objects as Instances of the classes
TrainData   = Data(dataPath + trainFile)
TestDat    = TestData(dataPath + testFile)
FcnsData    = IdealFunctions(dataPath + fcnsFile)
dummyTets = TestData(dataPath + trainFile)

[idFcnsDf, mseDf] = FcnsData.GetIdealFunctions(TrainData.df)


SegmentationCheck = TestDat.Segmentation(idFcnsDf)

# Store Data to Databese
dbName  = 'prg_python_database'
tab1    = 'tabelle_1'           # Tranings Daten
tab2    = 'tabelle_2'           # Ideale Funktionen
tab3    = 'tabelle_3'           # Test Daten

DB = DB_Handling(dbName)
#DB.Db_StoreTable(tab1, TrainData.df)
#DB.Db_StoreTable(tab2, FcnsData.df)
#DB.Db_StoreTable(tab3, TestData.df)

#tst = DB.DB_GetTable(tab1)     # for testing
