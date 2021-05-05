# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:38:28 2021

@author: rimes
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk
from InputWindow import UserInputWindow



def getUserInput(title, prompt):
    root = Tk()
    root.geometry("250x150+300+300")
    app = UserInputWindow(title, prompt)
    root.mainloop()
    return app.getValue()

def logIn(browser):
    UserEmail = getUserInput("Email Adress", "Please enter email adress:")    
        
    email = browser.find_element_by_tag_name('input')
    email.send_keys(UserEmail)
    nextBttn = browser.find_element_by_class_name("VfPpkd-RLmnJb")
    nextBttn.click()
            
    password = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='password']")))
    UserPassword = getUserInput("User Password", "Please enter your passoword:")
    password.send_keys(UserPassword)
    
    submit = browser.find_element_by_class_name('VfPpkd-RLmnJb')
    submit.click()
    
def sendEmail(browser):
    mail = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".gb_g")))
    mail.click()
    
    compose = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".z0")))
    compose.click()
    
    to = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".vO")))
    to.send_keys("example@gmail.com")
    subject = browser.find_element_by_class_name('aoT')
    subject.send_keys("Test 3")
    text = browser.find_element_by_css_selector('.Ar.Au')
    text.click()
    message = browser.find_element_by_css_selector('.Am.Al.editable.LW-avf.tS-tW')
    message.send_keys("Test -")
    send = browser.find_element_by_class_name("dC")
    send.click()

if __name__ == "__main__":
    browser = webdriver.Chrome()
    browser.get('https://google.com/')
    signIn = browser.find_element_by_link_text('Sign in')
    signIn.click()
    
    logIn(browser)
    sendEmail(browser)
    browser.close()
    

    
