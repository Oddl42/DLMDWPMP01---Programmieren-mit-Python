'''
---------------------------------
---       unittests           ---
---------------------------------
'''

from Bibs import unittest, np, pd,os
from Classes import Data, IdealFunctions, TestData, DB_Handling
        

class TestDataClass(unittest.TestCase):
    
    def test_Data_class(self):
        trainFile   = r'\train.csv'
        codePath    = os.getcwd()
        projectPath = os.path.dirname(codePath)
        dataPath    = projectPath + r'\DataSet'   
        self.assertEqual(self.data.datapath, dataPath+trainFile)
        self.assertTrue(os.path.exists(self.data.datapath))
        self.assertIsInstance(self.data.df, pd.DataFrame)
        
    def test_IdealFunctions_class(self):
        trainFile   = r'\train.csv'
        idealFile   = r'\ideal.csv'
        codePath    = os.getcwd()
        projectPath = os.path.dirname(codePath)
        dataPath    = projectPath + r'\DataSet'
        
        ideal_func = IdealFunctions(dataPath+idealFile)
        trainData = Data(dataPath+trainFile)
        result = ideal_func.GetIdealFunctions(trainData.df)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], pd.DataFrame)
        self.assertIsInstance(result[1], pd.DataFrame)

    def test_TestData_class(self):
        testFile   = r'\test.csv'
        codePath    = os.getcwd()
        projectPath = os.path.dirname(codePath)
        dataPath    = projectPath + r'\DataSet'
        
        test_data = TestData(dataPath+testFile)
        idFcnDf = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        result = test_data.Segmentation(idFcnDf)
        self.assertIsInstance(result, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
