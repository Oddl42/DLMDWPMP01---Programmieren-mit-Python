'''
-------------------------
---       main        ---
-------------------------

'''
# Import libs and Classes
from Bibs import pd, np, sys, mysql, os, figure, show, palettes
from Classes import Data, TestData, IdealFunctions, DB_Handling
# Init-Paths and Files
testFile    = r'\test.csv'              # Using Raw-String => r'\'
trainFile   = r'\train.csv'
fcnsFile    = r'\ideal.csv'

codePath    = os.getcwd()
projectPath = os.path.dirname(codePath)
dataPath    = projectPath + r'\DataSet'         


# Create Data-Objects as Instances of the classes
Train   = Data(dataPath + trainFile)
Test    = TestData(dataPath + testFile)
Fcns    = IdealFunctions(dataPath + fcnsFile)


[idFcnsDf, mseDf] = Fcns.GetIdealFunctions(Train.df)   # Get Ideal Functions for Training-Data 
SegmentationCheck = Test.Segmentation(idFcnsDf)    # Check the Ideal-Functions for Test-Data     

# Store Data to Databese
dbName  = 'prg_python_database'
tab1    = 'tabelle_1_Trainings_Daten'      # Traning-Data
tab2    = 'tabelle_2_Ideale_Funktionen'    # Ideal-Functions
tab3    = 'tabelle_3_Test_Daten'           # Test-Data

DB = DB_Handling(dbName)
DB.Db_StoreTable(tab1, Train.df)
DB.Db_StoreTable(tab2, Fcns.df)
DB.Db_StoreTable(tab3, SegmentationCheck)

tst = DB.DB_GetTable(tab3)     # Test: Getting Data from Database


# Plotting Data

colors = palettes.brewer['Paired'][idFcnsDf.columns.shape[0]]    # Create Colors by brewer palette      

ax = figure(width=500, height=500)
i = 0
for y in idFcnsDf.columns[1:]:
    ax.scatter(idFcnsDf['x'].values, idFcnsDf[y].values,size=3,color=colors[i])
    FiltDf = SegmentationCheck[SegmentationCheck[SegmentationCheck.columns[3]]==y]
    xFilt =  FiltDf['x'].values
    yFilt = FiltDf[FiltDf.columns[1]].values
    ax.scatter(xFilt, yFilt, size=5,color=colors[i], legend_label = y + '/Test Data', marker='plus')
    i=i+1


FiltDf = SegmentationCheck[SegmentationCheck[SegmentationCheck.columns[3]]=='Data out of range']
xFilt =  FiltDf['x'].values
yFilt = FiltDf[FiltDf.columns[1]].values   
ax.scatter(xFilt, yFilt, size=5, color='deeppink', legend_label = 'Out of Range', marker='plus')
show(ax)

