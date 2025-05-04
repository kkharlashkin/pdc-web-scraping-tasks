# Total flags 44/61

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
driver.get("https://hertie-scraping-website.vercel.app/")

flags_dicts = []

#Level1/
soup = BeautifulSoup(driver.page_source, "html.parser")

# Flags with nesting or in text-transparent (from Flag-1 till Flag-8)
flag_tags = soup.find_all("p", class_=lambda c: c and ("text-base" in c or "text-transparent" in c))
for tag in flag_tags:
    parent = tag.find_parent("div")
    while parent:
        parent_id = parent.get("id", "")
        if parent_id.startswith("nesting-"):
            flag = tag.get_text(strip=True)
            flags_dicts.append({"flag": flag})
            break
        parent = parent.find_parent("div")

# Flags with names hidden in the id attribute (Flag-9, Flag-11, etc.)
id_flags = soup.find_all("div", id=True)
for id in id_flags:
    id_val = id.get("id", "")
    if id_val.startswith("flag-"):
        try:
            number = int(id_val.split("-")[1])
            if number >= 9:
                flags_dicts.append({"flag": id_val})
        except ValueError:
            continue

# Flags with names hidden in the class attribute (Flag-10, Flag-12, etc.)
divs = soup.find_all("div", class_=True)
for div in divs:
    class_list = div.get("class", [])
    for class_name in class_list:
        if class_name.startswith("flag-") and class_name[5:].isdigit():
            flags_dicts.append({"flag": class_name})

#Level2/
driver.get("https://hertie-scraping-website.vercel.app/level2")
soup2 = BeautifulSoup(driver.page_source, "html.parser")

# Flag-41 in text
text_divs = soup2.find_all("div", class_="text-center my-4")
for div in text_divs:
    text = div.get_text(strip=True)
    if "flag-41" in text:
        flags_dicts.append({"flag": "flag-41"})

# Flag-42 in text-transparent
transparent_divs = soup2.find_all("div", class_="text-transparent")
for div in transparent_divs:
    text = div.get_text(strip=True)
    if text.startswith("flag-"):
        flags_dicts.append({"flag": text})

# Flag-43 and Flag-51 (accidentally scraped it) in id's
flag_id_tags = soup2.find_all("p", id=True)
for id in flag_id_tags:
    id_val = id.get("id", "")
    if id_val.startswith("flag-"):
        try:
            number = int(id_val.split("-")[1])
            if number >= 42:
                flags_dicts.append({"flag": id_val})
        except ValueError:
            continue

# Result
flags_dicts.sort(key=lambda x: int(x["flag"].split("-")[1]))

for flag in flags_dicts:
    print(flag)

driver.quit()