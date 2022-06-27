import requests
from datetime import timedelta, date
from twilio.rest import Client

account_sid = "account sid"
auth_token = "auth_token"
client = Client(account_sid, auth_token)

# ----------------------Get price-------------------------
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
yesterday = str(date.today() - timedelta(1))
before_yesterday = str(date.today() - timedelta(2))

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "api_key"
}

response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
data = response.json()
yest_close = float(data["Time Series (Daily)"][yesterday]["4. close"])
before_yest_close = float(data["Time Series (Daily)"][before_yesterday]["4. close"])
percent = round((yest_close - before_yest_close) / before_yest_close * 100, 1)

# ------------------------------Get news---------------------------

def calculate_percent():
    if percent < 0:
        return f"TSLA: ↓{percent}%"
    else:
        return f"TSLA: ↑{percent}%"


if percent < -0.3 or percent > 5:
    parameters_news = {
        "q": COMPANY_NAME,
        "apiKey": "api key"
    }
    response_news = requests.get("https://newsapi.org/v2/top-headlines", params=parameters_news)
    response_news.raise_for_status()
    data_news = response_news.json()
    articles = data_news["articles"]

    headline = {title["title"]: title["description"] for title in articles[:3]}
    print(headline)

    brief = [title["description"] for title in articles[:3]]
    print(brief)
# -------------------------------Send SMS-----------------
    for key, value in headline.items():
        message = client.messages.create(
                                      body=f'{calculate_percent()}\nHeadline: {key}\nBrief: {value}',
                                      from_='your phone',
                                      to='my phone'
                                  )

        print(message.status)

