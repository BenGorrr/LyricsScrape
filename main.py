# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
DRIVER_PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

""" useful attribute:
        element.tag_name
        element.text
        element.get_attribute('value')
"""

def exportText(filename, text):
    with open(filename, mode='w', encoding="utf-8") as file:
        file.write(text)

def mulanciGetLyric(name):
    url = "https://www.mulanci.org/zhs/search/#gsc.tab=0&gsc.q="

    driver.get(url+name)

    link_div = driver.find_element_by_class_name('gs-title')
    link_a = link_div.find_element_by_class_name('gs-title')
    link = link_a.get_attribute("data-ctorig")
    print(link)
    #driver.close()
    driver.get(link)
    try:
        content_div = driver.find_element_by_id('lyric-content')
        content = content_div.text
        exportText("text.txt", content)
    except NoSuchElementException:
        print("Can't find lyric")
        content = ""
    driver.close()
    return content

def filterLyric(lyrics, method=1):
    """ filter out unwanted text in the lyric list
        method 1 is for mulanci filtering
        method 2 is for kulanci filtering
    """
    if method == 1:
        for i in lyrics[10:]:
            if i.find("：") != -1:
                index = lyrics[10:].index(i) + 10
                lyrics = lyrics[:index]
                exportText("text.txt", "\n".join(lyrics))
                break
        for i in range(len(lyrics)):
            if lyrics[i] != '':
                if lyrics[i][0] == "[":
                    lyrics = lyrics[:i]
                    break
    elif method == 2:
        #list comprehension, for lyric in lyrics, if lyric start with '[', remove the first 9 characters
        # else lyric remains same
        lyrics = [lyric[10:] if lyric[0] == '[' else lyric for lyric in lyrics]
    exportText("text_filtered.txt", "\n".join(lyrics))
    return lyrics

def kugeciGetLyric(name):
    url = "https://www.kugeci.com/search?q="

    driver.get(url+name)
    try:
        link_a = driver.find_element_by_css_selector('#tablesort tbody tr td a')
        link = link_a.get_attribute("href")
        driver.get(link)
        content_div = driver.find_element_by_id("lyricsContainer")
        content = content_div.text
        exportText("text.txt", content)
    except NoSuchElementException:
        print("Can't find lyric")
        content = ""
    driver.close()
    return content

def getLyric(name, method):
    """ wrapper for different site scrap"""
    lyric = ""
    if method == 1:
        lyric = mulanciGetLyric(name)
    elif method == 2:
        lyric = kugeciGetLyric(name)

    if lyric != "":
        lyric = lyric.split("\n")
        lyric = filterLyric(lyric, method=method)
name = "why you gonna lie"

getLyric(name, 2)
