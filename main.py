# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
DRIVER_PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

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

def filterLyric(lyrics):
    """ filter out unwanted text in the lyric list """
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

    exportText("text_filtered.txt", "\n".join(lyrics))
    return lyrics



name = "真的傻"

lyric = mulanciGetLyric(name)
if lyric != "":
    lyric = lyric.split("\n")
    lyric = filterLyric(lyric)
