'''
---------------------------------
---       Classes File        ---
---------------------------------

* Data():
    Input: string of File-path
    - import Data from CSV file and store to pd DataFrame

* IdealFunctions()
    Child of Data
    - GetIdealFunctions:
        Input: DataFrame of Trainigs-Data
        Output: DataFrame of best fitting Ideal Funktion
        
* TestData()
    Child of Data
    - ValidateFunction:
        Input: DataFrame of 'Ideal Functions'
        Output: DataFrame wich maps the TestData to an Ideal-Input-Fcn
'''

from Bibs import pd, np, sys, mysql, db

# Class Data
class Data():
    def __init__(self, datapath):
        self.datapath = datapath
        try:
            self.df = pd.read_csv(datapath)
            self.df.set_index('x', inplace=True)
        except FileNotFoundError:
            print(sys.exc_info())
  
        cols = self.df.columns
        
        for i in cols:
            self.__dict__[i] = self.df[i]


# Class Ideal Functions child of Data
class IdealFunctions(Data):
    
    def __init__(self, datapath):
        Data.__init__(self, datapath)
    
    def GetIdealFunctions(self, dfTrain:pd.DataFrame):
        
        bestFitFcns = []
        bestFitError = []
        # Interate over all train - data
        for y in dfTrain.columns:
            error = pd.Series(np.zeros(self.df.shape[1]), index=self.df.columns)    # Initialize Error DF
            for idx in dfTrain[y].index:
                bestFitIdx = (abs((self.df.index - idx)))                           # get best Fit Index
                bestFitData = self.df.iloc[bestFitIdx.argmin()]                     # get best Fit Index Data
                y_diff = ((bestFitData.values - dfTrain[y][idx])**2)                # calcualte Square Error
                error[:] = error.values + y_diff                
            
            bestFitFcns.append(error.idxmin())
            bestFitError.append(error[error.idxmin()] / dfTrain[y].shape[0])
        
        ErrorDF = pd.DataFrame(bestFitError, index=bestFitFcns, columns=['mse'])
        FiltDf = self.df[ErrorDF.index]
        return [FiltDf, ErrorDF] 

# Class TestData child of Data
class TestData(Data):
    def __init__(self, datapath):
        Data.__init__(self, datapath)
    
    def Segmentation(self, idFcnDf:pd.DataFrame(), thereshold = np.sqrt(2)):
        
        data = []
        cols = []
        for y in self.df.columns:           # iterate over all Test-Data
            bestFitFcn = []
            distance = []
            checkDouble =[]
            for idx in self.df[y].index:    # iterate over all Points of Data 
                bestFitIdx = (abs((idFcnDf.index - idx)))              # get best Fit Index
                bestFitData = idFcnDf.iloc[bestFitIdx.argmin()]        # get best Fit Index Data
                if self.df[y][idx].size == 1:
                    y_diff = abs(bestFitData - self.df[y][idx])
                    if y_diff[y_diff.idxmin()] < thereshold:
                        distance.append(y_diff[y_diff.idxmin()])
                        bestFitFcn.append(y_diff.idxmin())
                    else:
                        distance.append(float('nan'))
                        bestFitFcn.append('Data out of range')
                else:
                    if idx not in checkDouble:
                        checkDouble.append(idx)
                        for i in range(self.df[y][idx].values.shape[0]):
                            y_diff = abs(bestFitData - self.df[y][idx].values[i])
                            if y_diff[y_diff.idxmin()] < thereshold:
                                distance.append(y_diff[y_diff.idxmin()])
                                bestFitFcn.append(y_diff.idxmin())
                            else:
                                distance.append(float('nan'))
                                bestFitFcn.append('Data out of range')
                                
            data.append(np.column_stack((self.df.index.values, self.df[y].values, distance, bestFitFcn)))
            cols.append(np.column_stack(('x ('+y + ')', y,'Delta Y ('+y + ')','Nummer Idaler Funktion ('+y + ')')))

        result = pd.DataFrame()
        for i in range(0,len(data)):
            for j in range(0,4):
                result[cols[i][0,:][j]] = data[i][:,j]

        return result
                
        
    def VaildationFunktion(self, dataFrame:pd.DataFrame, threshold= np.sqrt(2)):
        nTestPt = self.df.shape[0]
        nTests = self.df.shape[1]-1
        nFcn = dataFrame.shape[1]- 1
        nFcnPt = dataFrame.shape[0]
        check = np.zeros((nTestPt, nFcn))
        y_diff = []
        y_FcnId = []
        yFilt = []
        xFilt = []
        cols = self.df.columns
        
        for n in cols[1:]:
            for i in range(0, nTestPt):
                iX = np.abs(dataFrame['x'].values - self.df[cols[0]].values[i])
                idX = np.argmin(iX)
                dummy = np.zeros((nFcn,1))
                for j in range(0, nFcn):
                    y = dataFrame.columns[j+1]
                    yDiff = np.abs(dataFrame[y].values[idX] - self.df[n].values[i])
                    dummy[j] = yDiff
                    if yDiff < threshold:
                        check[i,j] = 1
                        
                if check[i,0:].any():
                    xFilt.append(self.df[cols[0]].values[i])
                    yFilt.append(self.df[n].values[i])
                
                y_diff.append(np.min(dummy))
                y_FcnId.append(dataFrame.columns[np.argmin(dummy)+1])
        
        dfFilt = pd.DataFrame({cols[0]:xFilt, cols[1]:yFilt})
        d = pd.DataFrame({'delta_Y': y_diff[0:], 'Ideal Fcn Index':y_FcnId})
        dfFiltTab = pd.concat([self.df,d],axis=1)
        return dfFilt, dfFiltTab

# Class Database Handling
class DB_Handling:
    def __init__(self, dbName):
       self.dbName = dbName
       self.databasePath = 'mysql+mysqlconnector://TestUser:MyT3st_SQL@localhost/' + self.dbName
       
    def Db_Connect(self):
        try: 
            my_db = mysql.connector.connect(host="localhost", user="TestUser", password="MyT3st_SQL") 
            my_cursor = my_db.cursor()
            my_cursor.execute("SHOW DATABASES")
            xInit = False
            for dat in my_cursor:
                if dat[0] == self.dbName:
                    xInit = True
                    break
            try:
                if not xInit:
                    print(DBErrorHandling(self.dbName,self.dbTableName).my_message1)
                    my_cursor = my_db.cursor()
                    createDataBase = "CREATE DATABASE "  + self.dbName
                    my_cursor.execute(createDataBase)
                    print(DBErrorHandling(self.dbName,self.dbTableName).my_message3)                  
            except DBErrorHandling:
                print(DBErrorHandling(self.dbName,self.dbTableName).my_message4)
            
        except DBErrorHandling:
            print(DBErrorHandling(self.dbName,self.dbTableName).my_message5)
            
    def Db_StoreTable(self, dbTableName, dataFrame:pd.DataFrame):
        self.dbTableName = dbTableName
        self.dataFrame = dataFrame
        try:
            self.Db_Connect()
            engine = db.create_engine(self.databasePath)
            #metadata = MetaData(bind=engine)
            dataFrame.to_sql(dbTableName, con=engine, if_exists='replace', index = False)
            engine.dispose()
        except DBErrorHandling:
            engine.dispose()
            print(DBErrorHandling(self.dbName, self.dbTableName).my_message8)
   
    
    def DB_GetTable(self, dbTableName):
        self.dbTableName
        try:
            self.Db_Connect()  
            engine = db.create_engine(self.databasePath)
            tableDF = pd.read_sql_table(self.dbTableName, engine, columns = None)
        except DBErrorHandling:
            print(DBErrorHandling().my_messageConError)
            
        return tableDF
        
        

class DBErrorHandling(Exception):
    def __init__(self, dbName, dbTable):
        my_message1 = 'Datenbank ' + dbName + ' existier nicht!'
        self.my_message1 = my_message1
        
        my_message2= 'Fehler beim Speichern von ' + dbTable +': Tabelle existiert nicht!' 
        self.my_message2 = my_message2
        
        my_message3 = 'Datenbank ' + dbName + ' erfolgreich erstellt'
        self.my_message3 = my_message3
        
        my_message4 = 'Fehler beim erstellen der Datenbank ' + dbName
        self.my_message4 = my_message4
        
        my_message5 = 'Fehler bei Datenbankcontrolle ' + dbName
        self.my_message5 = my_message5
        
        my_message6 = 'Speichern der Tabelle ' + dbTable + ' erfolgreich!'
        self.my_message6 = my_message6
        
        my_message7 = 'Tablle ' + dbTable + ' erfolgreich erstellt'
        self.my_message7= my_message7
        
        my_message8 = 'Fehler beim Speichern von ' + dbTable
        self.my_message8= my_message8
        
        
        
        