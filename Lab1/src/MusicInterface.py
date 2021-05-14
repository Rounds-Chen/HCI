from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os.path


class PlayMusic():
    def __init__(self, songName, driverPath):
        self.songName=songName
        self.chromeDriverPath=driverPath

    def play(self):
        chrome_driver = os.path.abspath(self.chromeDriverPath) # r"C:\Program Files (x86)\Google\Chrome\chromedriver.exe"
        print(chrome_driver)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome = webdriver.Chrome(executable_path=chrome_driver,options=options)

        url = "https://music.163.com/#/search/m/?s={}&type=1".format(self.songName)
        chrome.get(url)
        chrome.switch_to.frame("g_iframe")
        element=WebDriverWait(chrome, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.ply '))).click()

if __name__=="__main__":
    m=PlayMusic("gravity")
    m.play()
