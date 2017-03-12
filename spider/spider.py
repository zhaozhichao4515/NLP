#coding:utf-8
'''
    本爬虫负责对日语-英语双语语料的爬取，经过少量修改，能够爬取其他双语语料
'''
import urllib.parse
from bs4 import BeautifulSoup
import requests
import re
import csv
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

def writeCsv(url, fileNumber):
    try:
        url_list = []
        r = requests.get(url)
        page = []
        doc = r.text
        soup = BeautifulSoup(doc, "html.parser")
        # print(doc)
        # doc = r.text.encode(r.encoding).decode('gbk')

        tags = soup.find_all("p", "qotCE")
        tagj = soup.find_all("p", "qotCJ")

        fileName = 'weblio-'
        fileName += str(fileNumber)
        fileName += '.csv'

        csvFile = open(fileName, 'a', newline="", encoding='utf-8')

        try:
            writer = csv.writer(csvFile)

            list1 = []
            list2 = []

            for eache in tags:
                dr = re.compile(r'<[^>]+>', re.S)
                eache = dr.sub('', eache.text)
                eache = re.sub(' +', ' ', eache)
                eache = re.sub('\\n', '', eache)
                list1.append(eache)

            for eachj in tagj:
                dr = re.compile(r'<[^>]+>', re.S)
                eachj = dr.sub('', eachj.text)
                eachj = re.sub(' +', ' ', eachj)
                eachj = re.sub('\\n', '', eachj)
                list2.append(eachj)

            for x in range(len(tags)):
                list1[x] = list1[x].replace("');//-->", '')
                list1[x] = list1[x].replace("例文帳に追加", '')
                list1[x] = list1[x].replace(",", '')
                list1[x] = list1[x].replace("?", '')

                s = list2[x].split("-")
                list2[x] = s[0]
                list2[x] = list2[x].replace(",", '')
                list2[x] = list2[x].replace("?", '')
                # print(list1[x], list2[x], url)
                # print(list1[x],"------------" ,list2[x])

                writer.writerow((list1[x],list2[x],url))
                # pass


        except Exception:
            print("No data")
            pass
        finally:
            csvFile.close()
    except TimeoutException as e:
        # print(e)
        pass


# this is to define the url
def findUrl(letter):
    # https://bitex-cn.com/?m=Dic&a=search&dickeyword=关键词&currentpage=1
    # url = "http://bitex-cn.com/?m=Dic&a=search&dickeyword="
    # url += letter
    # url += "&currentpage=1"
    for i in range(1, 1000):
        pageNumber = i
        url = "http://ejje.weblio.jp/sentence/content/" +letter + "/" + "%s" % i
        print(url)
        # return url
        writeCsv(url, letter)
        r = requests.get(url)
        doc = r.text

        soup = BeautifulSoup(doc, "html.parser")
        line = soup.find_all("a")
        # print(line)

        mystring = "次へ＞"
        if mystring in doc:
            print("ok")
        else:
            break


def findWords():
    filename = 'dic.txt'
    lines = []
    with open(filename,'rt',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line[:len(line) - 1]
            lines.append(line)
    f.close()
    return lines


def selectLetter():
    lines = findWords()
    for line in lines:
        # print(line)
        findUrl(line)
        print(line, " OK!")
        # time.sleep(3)


if __name__ == '__main__':
    selectLetter()
