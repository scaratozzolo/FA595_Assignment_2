import requests
from bs4 import BeautifulSoup
import pandas as pd
import glob
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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

    pairs.to_csv("data/name_purpose_pairs.csv", index=False)
    return pairs


def combine_files():

    df = pd.DataFrame({"Company_Name":[], "Company_Purpose":[]})

    files = glob.glob("data/*.csv")
    for file in files:
        try:
            tempdf = pd.read_csv(file)
        except:
            tempdf = pd.read_csv(file, sep="\t")
        
        try:
            tempdf.columns = df.columns
        except:
            tempdf.drop("Unnamed: 0", axis=1, inplace=True)
            tempdf.columns = df.columns

        df = df.append(tempdf, ignore_index=True)

    return df


def perform_nlp(df):
    
    sid = SentimentIntensityAnalyzer()

    df["Sentiment"] = df["Company_Purpose"].apply(lambda x: sid.polarity_scores(x)['compound'])

    df.sort_values("Sentiment", ascending=False, inplace=True)

    df.head().to_csv("head.csv")
    df.tail().to_csv("tail.csv")
    df.to_csv("output.csv", index=False)
    return df



if __name__ == '__main__':

    # print(combine_files())
    perform_nlp(combine_files())
    # perform_nlp(combine_files())
    # print(pd.read_csv("data/fake_company.csv", sep="\t"))
