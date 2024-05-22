import snscrape.modules.twitter as sntwitter
import matplotlib.pyplot as pyplot
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from textblob import TextBlob

def validStockSymbol(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        history = stock_data.history(period='1y')
        return not history.empty
    except ValueError:
        return False
    
def sentimentAnalysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    polarity = sentiment.polarity

    return polarity
    
    
def lookup(symbol):
    tweets = []
    MAX_TWEETS = 100
    keyword = symbol
    positive = 0
    neutral = 0
    negative = 0

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    end_dateSTR = end_date.strftime('%Y-%m-%d')
    start_dateSTR = start_date.strftime('%Y-%m-%d')

    query = f"{keyword} since:{start_dateSTR} until:{end_dateSTR}"

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > MAX_TWEETS:
            break
        tweets.append({
            tweet.content
        })

    for tweet in tweets:
        rating = sentimentAnalysis(tweet)
        if (rating == 0):
            neutral += 1
        elif (rating == 1):
            positive += 1
        else:
            negative +=1

    print("Positive news: " + positive)
    print("Negative news: " + negative)
    print("Neutral news: " + neutral)

    positive_percentage = (positive / positive + neutral + negative) * 100
    print(f"The overall positivity of {symbol} is : {positive_percentage}")
        

    
def main():
    symbol_input = input("Input a valid stock symbol you wish to lookup: ")
    symbol_input.capitalize()

    if validStockSymbol(symbol_input):
        lookup(symbol_input)
    else:
        exit(0)

if __name__ == "__main__":
    main()



