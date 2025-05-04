# Total flags 40

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
driver.get("https://hertie-scraping-website.vercel.app/")

soup = BeautifulSoup(driver.page_source, "html.parser")

flags_dicts = []
# Flags with nesting - ...
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

# Flags with names hidden in the id attribute
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

# Flags with names hidden in the class attribute
divs = soup.find_all("div", class_=True)
for div in divs:
    class_list = div.get("class", [])
    for class_name in class_list:
        if class_name.startswith("flag-") and class_name[5:].isdigit():
            flags_dicts.append({"flag": class_name})

# Result

flags_dicts.sort(key=lambda x: int(x["flag"].split("-")[1]))

for flag in flags_dicts:
    print(flag)

driver.quit()