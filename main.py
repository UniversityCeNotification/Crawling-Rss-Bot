import json
import os
import feedparser
from pymongo import MongoClient
from dotenv import DotEnv
dotenv = DotEnv('.env')
client = MongoClient(dotenv.get('MongoDbUri', 'mongodb://localhost:27017'))
db = client[dotenv.get('MongoDbName', 'rsscrawler')] # which database
crawlers = db.crawlers  # which collection

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def crawlXpath():
    return

def crawlRss(url):
    if url == '' or not url.startswith('http'):
        print(bcolors.FAIL + 'Error: url can not be empty string or url should startwith http' + bcolors.ENDC)
        return
    d = feedparser.parse(url)
    for entry in d['entries']:
        data = {
            'title': entry['title'],
            'link': entry['link'],
            'status': 'new'
        }
        result = crawlers.find_one({'link': entry['link']})
        if not result:
            print('New Link crawled')
            crawlers.insert_one(data)

    print(bcolors.OKGREEN + '[-] Crawling Site Finished' + bcolors.OKGREEN)

if __name__ == '__main__':
    print(bcolors.OKBLUE + '\n[*] Program Started' + bcolors.ENDC)
    Files = ['sites/'+ File for File in os.listdir('sites') if File.endswith('.json')]
    print(Files)
    for File in Files:
        with open(File) as FileJsonData:
            d = json.load(FileJsonData)
            Site = d.get('Site', 'Nope')
            SiteLink = d.get('SiteLink', 'Nope')
            SiteRssLink = d.get('SiteRssLink', 'Nope')
            print(bcolors.OKGREEN + '[+] Crawling Site:\n'+
                ' SiteName: ' + Site +
                ' | SiteLink: ' + SiteLink +
                ' | SiteRssLink: ' + SiteRssLink + bcolors.ENDC)
            if not SiteRssLink == '':
                crawlRss(SiteRssLink)
            else:
                crawlXpath(d)
