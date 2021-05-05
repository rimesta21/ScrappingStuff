# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:28:00 2021

@author: rimes
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import requests, os, bs4
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.action_chains import ActionChains
import time
from tkinter import Tk
from InputWindow import UserInputWindow

"Code gotten from https://www.thepythoncode.com/article/download-web-page-images-python"

def getUserInput(title, prompt):
    root = Tk()
    root.geometry("250x150+300+300")
    app = UserInputWindow(title, prompt)
    root.mainloop()
    return app.getValue()

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    #if not a valid url these two will be empty returning false
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_img(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    img = soup.find("img")
    img_url = img.attrs.get("src")
    #if we can't find it's src then we don't get the image
    if not img_url:
        return
    #merges with the base url
    img_url = urljoin(url, img_url)
    #gets ride of the "HTTP GET" key value pairs
    try:
        pos = img_url.index("?")
        img_url = img_url[:pos]
    except ValueError:
        pass
    #make sure it is a value url
    if is_valid(img_url):
        return img_url
    return

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately (stream downloads it in chunks)
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
            
def searchImages(browser, SearchTerm):
    cont = True
    while cont:
        try:
            searchIcon = browser.find_element_by_class_name("icon-search")
            searchIcon.click()
            search = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.ID,"search-field")))
            search.send_keys(SearchTerm)
            search.send_keys(Keys.ENTER)
            cont = False
        except TimeoutException:
            browser.refresh()
    

def getToFirstImg(browser):
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".view.photo-list-photo-view.awake")))
    firstImg = browser.find_element_by_xpath("(//div[@class = 'photo-list-photo-interaction'])[1]")
    action = ActionChains(browser)
    browser.execute_script("window.scrollTo(0, 50)") 
    action.move_to_element(firstImg).click().perform()
    WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.hide-text')))

def getXnumImg(browser, numPics):
    urls = []
    #creates a progress bar and finds all the images' urls
    pbar = tqdm(total = 10 , desc = "Downloading images...")
    i = 0 
    while i < numPics:
        try:
            WebDriverWait(browser,3).until(EC.presence_of_element_located((By.LINK_TEXT, "Sponsored Advertiser")))
            time.sleep(8)
        except TimeoutException:
            imgURL = get_img(browser.current_url)
            if imgURL != None:
                urls.append(imgURL)  
            pbar.update(1)
            i += 1
            
        if i < 2:    
            nextImg = browser.find_element_by_class_name("hide-text")
        else:
            nextImg = browser.find_element_by_xpath("(//span[@class = 'hide-text'])[2]")
        nextImg.click()
    return urls

if __name__ == "__main__":
    SearchTerm = getUserInput("Search Word", "Please enter what you want to search:")
    numOfPictures = getUserInput("Number of Pictures", "Please enter the number of pictures you want:")
    browser = webdriver.Chrome()
    browser.get('https://flickr.com/')
    searchImages(browser,SearchTerm)
    getToFirstImg(browser)
    urls = getXnumImg(browser, int(numOfPictures))
    browser.close()
    for link in urls:
        download(link, "pictures")
    
    
    
    
        
        
    