from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver")
browser.get(starturl)
time.sleep(10)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []

def scrape() :
    for i in range(1,100):
        while(True):
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            c = int(soup.find_all("input" , attrs = {"class", "page_num" })[0].get("value"))
            if c < i :
                browser.find_element("xpath","/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
            elif c > i :
                browser.find_element("xpath","/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a").click()
            else :
                break
        for j in soup.find_all("ul",attrs = {"class","exoplanet"}) :
            litags = j.find_all("li")
            templist = []
            #enumerate is a function that returns the index along with the element.
            for index,s in enumerate(litags):
                if index == 0 :
                    templist.append(s.find_all("a")[0].contents[0])
                else :
                    try:
                        templist.append(s.contents[0])
                    except:
                        templist.append("")
            hyperlink_tag  = litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlink_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(templist)
    browser.find_element("xpath","/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
    print(f"{i} page done")
    
def scrape_more(hyperlink) :
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        templist = []
        for m in soup.find_all("tr",attrs = {"class" , "fact_row"}):
            tdtags = m.find_all("td")
            for n in tdtags:
                try:
                    templist.append(n.find_all("div" , attrs = {"class","value"})[0].contents[0])
                except:
                    templist.append("")
        new_planet_data.append(templist)
    except:
        time.sleep(1)
        scrape_more(hyperlink)

scrape()
for index,data in enumerate(planet_data):
    scrape_more(data[5])
final_planet_data = []
for index,data in enumerate(planet_data):
    e = new_planet_data[index]
    e = [elem.replace("\n","") for elem in e ]
    e = e[:7]
    final_planet_data.append(data+e)
with open("scraper2.csv","w") as f:
    c = csv.writer(f)
    c.writerow(headers)
    c.writerows(final_planet_data)