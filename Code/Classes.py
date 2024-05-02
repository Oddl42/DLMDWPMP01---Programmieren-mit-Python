'''
---------------------------------
---       Classes File        ---
---------------------------------
'''

from Bibs import pd, np, sys, mysql, db, sqlite3

# Class Data
class Data():
    """
   This class is used to import data from a CSV file and store it in a 
   pandas DataFrame.
   """
    def __init__(self, datapath):
        """
        Initialize the Data class with the path to the data file.
        Parameters:
        datapath (str): The path to the data file.
        """
        self.datapath = datapath
        try:
            # write csv Data into DataFrame
            self.df = pd.read_csv(datapath)                
            #self.df.set_index('x', inplace=True)
            cols = self.df.columns
            for i in cols:
                self.__dict__[i] = self.df[i]

        except FileNotFoundError:
            print(sys.exc_info())
  


class IdealFunctions(Data):
    """
    This class is a child of the Data class. It is used to get the best 
    fitting functions from a DataFrame.
    """
    def __init__(self, datapath):
        """
       Initializes the IdealFunctions class with the given datapath.

       Parameters:
           - datapath (str): The path to the data.

       """
        Data.__init__(self, datapath)
    
    def GetIdealFunctions(self, dfTrain:pd.DataFrame):
        """
        Get the best fit function from an input DataFrame (Training Data).

        Parameters:
            - dfTrain (pd.DataFrame): The input Training DataFrame.

        Returns:
            - list: A DataFrame of the best fit functions, and a 
            DataFrame of the FunctionNumber with the MSE.

        Raises:
            - Errors: If there is an error during the process of 
            getting the best fit functions.
        """
        try:
            bestFitFcns = []
            bestFitError = []
            # Interate over all train - data
            for y in dfTrain.columns[1:]:
                # Initialize Error DF
                error = pd.Series(np.zeros(self.df.shape[1]-1), index=self.df.columns[1:])   
                for idx, row in dfTrain[['x',y]].iterrows():
                    # get best Fit X- Value
                    bestFitIdx = (abs((self.df['x'] - row['x'])))  
                    # get Y-Values to best Fit X-Value
                    bestFitData = self.df.iloc[bestFitIdx.argmin()]
                    # calc Square Error (without X)
                    y_diff = ((bestFitData.drop('x').values - row[y])**2)   
                    error[:] = error.values + y_diff                
                # get best fit function
                bestFitFcns.append(error.idxmin())                                  
                try:
                    # calc mean square error
                    bestFitError.append(error[error.idxmin()] / dfTrain[y].shape[0])     
                except ZeroDivisionError():
                    print(ZeroDivisionError())
            
            ErrorDF = pd.DataFrame(bestFitError, index=bestFitFcns, columns=['mse'])
            FiltDf = pd.concat([self.df['x'],self.df[ErrorDF.index]],axis=1)
            return [FiltDf, ErrorDF] 
        except Errors:
            print(Errors().my_message1)
            
# Class TestData child of Data
class TestData(Data):
    """
    This class is a child of the Data class. It is used to segment the test data.
    """
    def __init__(self, datapath):
        Data.__init__(self, datapath)
    
     # Function:   
    def Segmentation(self, idFcnDf:pd.DataFrame(), threshold = np.sqrt(2)):
        """
        Segment the test data based on the ideal functions and a threshold.

        Parameters:
            - idFcnDf (pd.DataFrame): The DataFrame of ideal functions.
            - threshold (float): (optional) The threshold for segmentation. 
            Default is sqrt(2).

        Returns:
            - DataFrame: The segmented test data, which assigns the 
            test data to an ideal function if the distance (Test - Fcn) < threshold.

        Raises:
            - Errors: If there is an error during the segmentation process.
        """
        try:
            result      = self.df.sort_values(['x'])
            minDist     = []
            bestFitFcn  = []
            for idx, row in result.iterrows():
                distance = []
                for y in idFcnDf.columns[1:]:
                    # get squared X- Error
                    bestFitIdx = (idFcnDf['x'] - row['x'])**2 
                    # get squared Y- Error
                    bestFitData = (idFcnDf[y] - row['y'])**2
                    # get squared Error / Distance
                    distance.append(np.sqrt(bestFitIdx + bestFitData).min())       
                if min(distance) < threshold:
                    # get min squared Error
                    minDist.append(min(distance)) 
                    # get best Fit Function                                  
                    bestFitFcn.append(idFcnDf.columns[distance.index(min(distance)) + 1])  
                else:
                    minDist.append(min(distance))
                    bestFitFcn.append('Data out of range')
        
            result['Delta'] = minDist
            result['Nummer Ideale Funktion'] = bestFitFcn
            return result        
        except Errors:
            print(Errors().my_message2)
            
    
# Class Database Handling
class DB_Handling:
    '''
    DB Handling:
        Connect to a Database
        Store Data (Tabel) to a Database
        Get Data (Tabel) from a Database
    '''
    def __init__(self, dbName):
        '''
        Initializes the DB_Handling class with the given database name.
    
        Parameters:
            - dbName (str): The name of the database.
        '''
        self.dbName = dbName
        #self.databasePath = 'mysql+mysqlconnector://TestUser:MyT3st_SQL@localhost/' 
        self.databasePath = 'sqlite:///' + self.dbName
        
    def Db_Connect(self):
        '''
        Connects to the database.

        Raises:
            - DBErrorHandling: If there is an error connecting to the database.
        '''
        try:
            # Connection to SQLite
            my_db = sqlite3.connect(self.dbName)
            my_cursor = my_db.cursor()
            my_db.close()
        
            # Connection to MySQL        
            '''
            my_db = mysql.connector.connect(host="localhost", 
                user="TestUser", password="***") 
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
            my_db.close()
            '''
        except DBErrorHandling:
            print(DBErrorHandling(self.dbName,self.dbTableName).my_message5)
        
            
    def Db_StoreTable(self, dbTableName, dataFrame:pd.DataFrame):
        '''
        Stores a table in the database.

        Parameters:
            - dbTableName (str): The name of the table.
            - dataFrame (pd.DataFrame): The data to be stored in the table.

        Raises:
            - DBErrorHandling: If there is an error connecting to the 
            database or storing the table.

        '''
        self.dbTableName = dbTableName
        self.dataFrame = dataFrame
        try:
            self.Db_Connect()
            engine = db.create_engine(self.databasePath)
            dataFrame.to_sql(dbTableName, con=engine, if_exists='replace', 
                             index = False)
            engine.dispose()
        except DBErrorHandling:
            engine.dispose()
            print(DBErrorHandling(self.dbName, self.dbTableName).my_message8)
   
    
    def DB_GetTable(self, dbTableName):
        '''
        Retrieves a table from the database.

        Parameters:
            - dbTableName (str): The name of the table to retrieve.

        Returns:
            - tableDF (pd.DataFrame): The retrieved table.

        Raises:
            - DBErrorHandling: If there is an error connecting to the database 
            or retrieving the table.

        '''
        self.dbTableName
        try:
            self.Db_Connect()  
            engine = db.create_engine(self.databasePath)
            tableDF = pd.read_sql_table(self.dbTableName, engine, columns = None)
            engine.dispose()
        except DBErrorHandling:
            engine.dispose()
            print(DBErrorHandling().my_messageConError)
            
        return tableDF

class Errors(Exception):
    '''
    Error of Functions
    '''
    def __init__(self):
        self.my_message1 = 'Best Fit Functions Error'
        self.my_message2 = 'Segmentation Error'                

class DBErrorHandling(Exception):
    '''
    Error of DbHandling
    '''
    def __init__(self, dbName, dbTable):
        my_message1 = 'Datenbank ' + dbName + ' existier nicht!'
        self.my_message1 = my_message1
        
        my_message2= 'Fehler beim Speichern von ' + dbTable +': Tabelle existiert nicht!' 
        self.my_message2 = my_message2
        
        my_message3 = 'Datenbank ' + dbName + ' erfolgreich erstellt'
        self.my_message3 = my_message3
        
        my_message4 = 'Fehler beim erstellen der Datenbank ' + dbName
        self.my_message4 = my_message4
        
        my_message5 = 'Fehler beim Verbinden mit Datenbank ' + dbName
        self.my_message5 = my_message5
        
        my_message6 = 'Speichern der Tabelle ' + dbTable + ' erfolgreich!'
        self.my_message6 = my_message6
        
        my_message7 = 'Tablle ' + dbTable + ' erfolgreich erstellt'
        self.my_message7= my_message7
        
        my_message8 = 'Fehler beim Speichern von ' + dbTable
        self.my_message8= my_message8
        
        
        
        