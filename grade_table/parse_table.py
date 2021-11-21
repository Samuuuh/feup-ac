import pandas as pd
from bs4 import BeautifulSoup as bs

DELIMITER = ";"

def read_table():
    f = open("./table.html", "r")
    return bs(f.read())

def translate_table(soup: bs) -> str: 
    csv = ""
    rows = soup.find_all("tr", {"class": "criterion"}) 
    for row in rows:   
        # title
        title = get_title(row) 
        if title != "" and title != None:
            csv += title + DELIMITER
        
        # columns 
        status = get_fields(row)
        status_csv = get_status_csv(status)
        csv += status_csv + "\n"  

    return csv


def get_title(row: bs):
    return row.find("td").text.strip()

def get_fields(row: bs):
    return row.find("td", {"class": "levels"})

def get_status_csv(status: bs):
    csv = ""
    tds = status.find_all("td", {"class": "level"})
    for td in tds:
        
        csv += get_status_tds(td, td['aria-checked']) + DELIMITER
    return csv[:-1]

def get_status_tds(td: bs, checked: str):
    definition = td.find("div", {"class": "definition"}).text.strip()
    score = td.find("div", {"class": "score"}).text.strip()
    text = f"{definition} ({score})" 
    if checked == "true": 
        return text + "[x]"
    return text




if __name__ == '__main__':
    soup = read_table()
    print(translate_table(soup))

