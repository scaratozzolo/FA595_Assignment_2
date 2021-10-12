import requests
from bs4 import BeautifulSoup
import pandas as pd


def create_company_pairs(num_pairs=50):
    pairs = pd.DataFrame({"Company_Name":[], "Company_Purpose":[]})

    i = 0
    while i < num_pairs:

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

    pairs.to_csv("name_purpose_pairs.csv", index=False)
    return pairs