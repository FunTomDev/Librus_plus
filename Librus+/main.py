from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_auto_update import check_driver
import os
from getpass import getpass
import time
import requests
import json

class Librus():
    def __init__(self, login, password):
        self.path = os.path.dirname(__file__)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(os.path.join(self.path, "src/webdriver/chromedriver.exe"), options=self.options)
        self.driver.get("https://adfslight.vulcan.net.pl/radomprojekt/LoginPage.aspx")
        self.end = False
        while self.end == False:
            try:
                self.loginField = self.driver.find_element(By.ID, "Username")
                self.passwordField = self.driver.find_element(By.ID, "Password")
                self.loginField.send_keys(Keys.CONTROL + 'a')
                self.loginField.send_keys(Keys.DELETE)
                self.loginField.send_keys(login)
                self.passwordField.send_keys(Keys.CONTROL + 'a')
                self.passwordField.send_keys(Keys.DELETE)
                self.passwordField.send_keys(password)
                self.driver.find_element(By.CLASS_NAME, "submit-button").click()
                element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="box"]/div[4]/label')) or EC.visibility_of_element_located((By.XPATH, '//*[@id="body"]/table')))
                self.end = True
            except:
                while True:
                    self.ans = input("You entered wrong data.\nDo you want to try again? (Y/N): ")
                    if self.ans.upper() == "Y":
                        login = input("Enter your login: ")
                        password = getpass("Enter your password: ")
                        break
                    elif self.ans.upper() == "N":
                        self.end = True
                        self.driver.close()
                        break
                    else:
                        print("Wrong answer, try again")
        self.driver.get("https://portal.vulcan.net.pl/jst/radomprojekt/rejestr.aspx")
        self.driver.find_element(By.XPATH, '//*[@id="ctl00_AppEnvironment_Header"]/div/a[9]').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "warning-close")))
        self.driver.find_element(By.CLASS_NAME, "warning-close").click()
    def get_grades(self):
        self.fullDict = {}
        self.grades0 = self.driver.find_elements(By.CLASS_NAME, "line0")
        self.grades1 = self.driver.find_elements(By.CLASS_NAME, "line1")
        self.temp = []
        for grade in self.grades0:
            try:
                grade.find_element(By.CSS_SELECTOR, "img[src='/images/tree_colapsed.png']")
                self.temp.append(grade)
            except:
                pass
        self.grades0 = self.temp
        self.temp = []
        for grade in self.grades1:
            try:
                grade.find_element(By.CSS_SELECTOR, "img[src='/images/tree_colapsed.png']")
                self.temp.append(grade)
            except:
                pass
        self.grades1 = self.temp
        self.temp = []
        self.grades = self.grades0 + self.grades1
        for grade in self.grades:
            self.gradesDict = {}
            self.subjectName = grade.find_elements(By.TAG_NAME, "td")[1].text
            self.subjectGrades = [x.text for x in grade.find_elements(By.TAG_NAME, "td")[2].find_elements(By.TAG_NAME, "span")]
            self.subjectAvg = grade.find_elements(By.TAG_NAME, "td")[3].text
            self.gradesDict['Grades'] = self.subjectGrades
            self.gradesDict['Grades average'] = self.subjectAvg
            self.fullDict[self.subjectName] = self.gradesDict
        self.fullDict = json.dumps(self.fullDict, indent=4)
        return self.fullDict
            
            
        
def checkDriver():
    path = os.path.dirname(__file__)
    check_driver(os.path.join(path, "src\webdriver"))
def main():
    checkDriver()
    login = input("Enter your login: ")
    password = getpass("Enter your password: ")
    librus = Librus(login,password)
    print(librus.get_grades())

if __name__ == '__main__':
    main()