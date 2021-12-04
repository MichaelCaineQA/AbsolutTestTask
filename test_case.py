import time
import unittest
from unittest import result
from unittest.case import skip
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CheckInsurancePremiumAndCalcNum(unittest.TestCase):
    

    def setUp(self):
        self.page = webdriver.Chrome(ChromeDriverManager().install())
        self.page.set_window_size(1920, 1080)


    def test_01(self):
        page = self.page
        page.get(
            "https://old.absolutins.ru/kupit-strahovoj-polis/strahovanie-zhizni-i-zdorovya/ukus-kleshcha/"
        ) # 1. Переходим на проверяемую страницу
        
        # Так как эти поля изначально что-то в себе содержат, записываем их значения для дальнейшего сравнения
        initial_result_sum = page.find_element(By.XPATH, "//span[@id='result-sum']").text 
        initial_result_number = page.find_element(By.XPATH, "//span[@id='result-number']").text

        WebDriverWait(page, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@class='form-radio-list']/li[2]"))
        )
        page.find_element(By.XPATH, "//ul[@class='form-radio-list']/li[2]").click() # 2. Выбираем количество застрахованных лиц

        WebDriverWait(page, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-target='ak2']"))
        )
        page.find_element(By.XPATH, "//div[@data-target='ak2']").click() # 3. Выбираем подтип страхования
        
        WebDriverWait(page, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@role='combobox']"))
        )
        page.find_element(By.XPATH, "//span[@role='combobox']").click() # 4. Раскрываем выпадающий список регионов обслуживания
        
        WebDriverWait(page, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@id='region-menu']/li/div[contains(text(), 'г. Краснодар')]"))
        )
        page.find_element(By.XPATH, "//ul[@id='region-menu']/li/div[contains(text(), 'г. Краснодар')]").click() # 5. Выбираем регион обслуживания
        
        WebDriverWait(page, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='PROMOCODE']"))
        )
        page.find_element(By.XPATH, "//input[@name='PROMOCODE']").clear() # 6. Поле "Промокод" оставляем пустым, даже если в него было что-то введено
        
        WebDriverWait(page, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        page.find_element(By.XPATH, "//button[@type='submit']").click() # 7. Кликаем на кнопку "Рассчитать"

        time.sleep(0.1)
        WebDriverWait(page, 5).until_not(
            EC.presence_of_element_located((By.XPATH, "//div[@class='calc-col calc-col-float fixed loading']"))
        )
        actual_result_sum = page.find_element(By.XPATH, "//span[@id='result-sum']").text # 8. Записываем значение результатов рассчёта
        actual_result_number = page.find_element(By.XPATH, "//span[@id='result-number']").text # 9. Записываем значение номера рассчёта

        # Сравниваем текущее значение с имеющимся на странице изначально. Значение должно поменяться
        self.assertNotEqual(initial_result_sum, actual_result_sum)
        self.assertNotEqual(initial_result_number, actual_result_number)  


    def tearDown(self):
        self.page.close() 


if __name__ == '__main__':
    unittest.main()