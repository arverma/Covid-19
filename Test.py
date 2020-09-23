import unittest
import pandas as pd
import requests
from Analysis import covid19Data
from datetime import date, timedelta
from main import geturl


# url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2017HotfixDev9/v3/en-us/applemobilitytrends-2020-09-19.csv"
url = geturl()
get_url = requests.get(url)
obj = covid19Data(get_url)

today  = date.today()-timedelta(days=2)
nameOfDownloadFile = f"Downloaded-{today}.csv"


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)


    def test1(self):
        result = obj.run()
        self.assertEqual(result,True)


    # test for getDataFrame function wheather it is return a dataFrame or not
    def test2(self):
        result = obj.getDataFrame()[1]
        self.assertEqual(result, True)

    def test3(self):
        result = obj.getDataFrame()[1]
        self.assertTrue(result)

    # test for reArrangeDataFrame function wheather it is successfuly convert some column into rows
    def test4(self):
        dataFrame = pd.read_csv(nameOfDownloadFile,low_memory=False)
        result = obj.reArrangeDataFrame(dataFrame)[1]
        self.assertEqual(result,True)

    # test for run function
    def test5(self):
        result = obj.run()
        self.assertNotEqual(result,False)


    # create a temp CSV file which contains only 3 column
    # test if a csv contain less than required column then it's working or not
    def test6(self):
        dataFrame = pd.read_csv("temp.csv")
        result = obj.reArrangeDataFrame(dataFrame)[1]
        self.assertEqual(result, False)


    def test7(self):
        date = obj.validate("2020-12-12")
        self.assertEqual(date, 1)

        date = obj.validate("2020-20-30")
        self.assertNotEqual(date, 1)

        date = obj.validate("columnName")
        self.assertEqual(date, 0)



if __name__ == '__main__':
    unittest.main()
