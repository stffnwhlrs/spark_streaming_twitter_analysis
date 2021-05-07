import pandas as pd
import requests

#df = pd.read_csv("data_powerbi_test.csv")
#data = df.to_json(orient="records")
#print(data)


# for index, row in df.iterrows():
#     message 
#     print(row["message"], row["number"])
    

# REST POSt

url = "https://api.powerbi.com/beta/73458443-1627-4091-8b39-2222134907c5/datasets/20792726-b470-438e-a12c-6c99b9bba033/rows?key=p9e7FOz8G%2FkXhiHCGQ1rzm1MydzL8r26XyMdMcFcRMFWY4h6sUv4uatSqNQeR36ZC0%2FFDNwTbxsFJzboM57bZg%3D%3D"

data = [
    {
    "company" :"apple",
    "tweet_count" :120,
    "sentiment_positive" :0.3,
    "sentiment_negative" :0.7,
    "time" :"2021-05-04T13:45:52.819Z",
    "misc_text" :"",
    "misc_num" :0
    }
]


response = requests.post(url,json=data)
print(response)




