import pandas as pd
import requests

#df = pd.read_csv("data_powerbi_test.csv")
#data = df.to_json(orient="records")
#print(data)


# for index, row in df.iterrows():
#     message 
#     print(row["message"], row["number"])
    

# REST POSt

url = "https://api.powerbi.com/beta/73458443-1627-4091-8b39-2222134907c5/datasets/f2e292d5-75ab-4b9d-a2ef-fc665f46fa2b/rows?key=%2FTJsbiDXoLOO%2F1pwvhya4PhEvUtBn%2BYG9MwqAVKS494Ei4g%2FC9kRWB9vpkva2MO4BJQWzWfy0hmSLsk8Bg6AFg%3D%3D"

data = [
    {
    "message": "1111",
    "number": 2
    }
]


response = requests.post(url,json=data)
print(response)




