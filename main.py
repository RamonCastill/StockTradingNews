import requests
from twilio.rest import Client

AV_API_KEY = "YOURS"
AV_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_APY_KEY = "YOURS"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
account_sid = "YOURS"
auth_token = "YOURS"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

news_parameters = {
    "q": COMPANY_NAME,
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_APY_KEY
}
av_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": AV_API_KEY
}

response = requests.get(url=AV_ENDPOINT, params=av_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

data_yesterday = float(data_list[0]["4. close"])
data_before_yesterday = float(data_list[1]["4. close"])
difference = data_yesterday - data_before_yesterday
variation = abs(round((difference / data_yesterday) * 100))
if difference > 0:
    UPPER = "+"
else:
    UPPER = "-"

if variation >= 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    for new in news_data[:3]:
        client = Client(account_sid, auth_token)
        print(new)

        message = client.messages \
            .create(
            body=f"{STOCK}: {UPPER}{variation}%\n\n{new['title']}\n\n{new['description']}",
            from_='+14242066922',
            to='+56962328152'
        )

        print(message.sid)
