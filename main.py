import requests
from bs4 import BeautifulSoup
import pandas as pd

pairs = pd.DataFrame({"Company_Name":[], "Company_Purpose":[]})

i = 0
while i < 50:

    try:
        r = requests.get("http://3.85.131.173:8000/random_company")
    except Exception as e:
        print(e)
        print("request failed")

    soup = BeautifulSoup(r.content, "lxml")
    lis = soup.find_all("li")
    company_info = {i.decode_contents().split(":")[0].strip():i.decode_contents().split(":")[1].strip() for i in lis}

    pairs = pairs.append(pd.DataFrame({"Company_Name":[company_info["Name"]], "Company_Purpose":[company_info["Purpose"]]}), ignore_index=True)

    i += 1

print(pairs)
pairs.to_csv("name_purpose_pairs.csv", index=False)