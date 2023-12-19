import requests
from bs4 import BeautifulSoup
import json
import time

def find_wikipedia(artist_name) :
    url = ("https://google.com/search?q=" + artist_name + " artist wikipedia").replace(" ", "+")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("a")
    for result in results :
        if "wikipedia.org" in result["href"] :
            found = result["href"]
            found = found[found.index("https") : found.index("&sa")]
            return found.replace("%25", "%") #fixing weird glitch where %25 is used instead of % in url

def clean_label(label) : #fixing formatting issues, like citiations, and removing extra text (ex. ['KQ\xa0[ko]', 'Legacy', 'RCA[1][2]', 'Nippon Columbia[3]'] -> ['KQ', 'Legacy', 'RCA', 'Nippon Columbia'])
    if ("[" in label) :
        label = label[:label.index("[")]
    label = label.replace("\xa0", " ").strip()
    if ("Warner" in label) :
        label = "Warner Bros"
    if ("Columbia" in label) :
        label = "Columbia"
    if ("RCA" in label) :
        label = "RCA"
    return label


def extract_labels(wikipedia_url) :
    page = requests.get(wikipedia_url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="infobox biography vcard")
    if (results == None) :
        results = soup.find(class_="infobox vcard plainlist")
    labels = results.find_all("th", scope="row")
    found_section = ""
    for label in labels :
        if (label.text.strip() == "Labels") :
            found_section = label.parent
    results = found_section.find_all("li") + found_section.find_all("a")
    labels = []
    for result in results :
        found_label = clean_label(result.text.strip())
        if (found_label not in labels and len(found_label) > 0) :
            labels.append(found_label)
    return labels

def main() :
    url = "https://www.billboard.com/charts/artist-100/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    names = []

    #retrieving first artist (special element on website so it appears bigger)
    results = soup.find_all("h3", id="title-of-a-story")
    name = results[4].text.strip()
    names.append(name)
    #retrieving first artist (special element on website so it appears bigger)

    #retrieve the rest of the artists
    results = soup.find_all(class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-050 lrv-u-padding-l-1@mobile-max")

    for result in results :
        name = result.find("h3", id="title-of-a-story").text.strip()
        names.append(name)
    #retrieve the rest of the artists
        
    #retrieve labels and create JSON
    data = {}
    for name in names :
        time.sleep(1)
        data[name] = []
        try :
            wikipedia_url = find_wikipedia(name)
            labels = extract_labels(wikipedia_url)
            print(name + " : " + str(labels))
            data[name] = labels
        except :
            print(name + " : " + " failed.")
            data[name] = []
    #retrieve labels and create JSON
    
    #write JSON to file
    with open("labels.json", "w") as outfile :
        json.dump(data, outfile, indent=4)
    #write JSON to file
        
    #write to labels.js
    cur_date = time.strftime("%m/%d")
    f = open("labels.js", "w")
    f.write("var data = ")
    f.write(json.dumps(data))
    f.write(";")
    f.write("var lastUpdated = " + "\"" + cur_date + "\";")
    f.close()
    #write to labels.js

main()