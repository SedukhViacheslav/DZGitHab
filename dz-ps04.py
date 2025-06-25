from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("https://wiki.microinvest.su")
#В кавычках указываем URL сайта, на который нам нужно зайти
time.sleep(10)
#Задержка в 10 секунд
browser.quit()
#Закрываем браузер