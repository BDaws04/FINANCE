import yfinance as yf
import tkinter as tk
import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def getBB(data):
    global BB_mean, BB_upper, BB_lower
    closing_prices = data['Close'].sum()
    standard_deviation = data['Close'].std()
    BB_mean = round(closing_prices / len(data['Close']))
    BB_upper = round(BB_mean + standard_deviation + standard_deviation)
    BB_lower = round(BB_mean - standard_deviation - standard_deviation)

def getSMA(data):
    global SMA
    if len(data['Close']) < 5:
        return "Null"
    else:
        return round(data['Close'].sum() / len(data['Close']))
        
def priceChange(start, end):
    firstData = yf.download(stockSymbol, start=start, end=start)
    lastData = yf.download(stockSymbol, start=end, end=end)

    if len(firstData) == 0 or len(lastData) == 0:
        return "Null"
    else:
        firstPrice = firstData['Close'].sum()
        lastPrice = lastData['Close'].sum()
        
        return round(((lastPrice - firstPrice) / firstPrice) * 100, 2)
    
def calculatePERatio(symbol):
    data = yf.Ticker(symbol)

    current_price = data.history(period='1d')['Close'].iloc[-1]

    earnings_per_share = data.info['trailingEps']

    if earnings_per_share == None:
        return "Null"
    else:
        return round(current_price / earnings_per_share, 2)



def main():
    makeGUI()
   
   
def goBack(root):
    makeFirstPane(root)

def getStockData(stockSymbol, startDate, endDate):
    stockData = yf.download(stockSymbol, start=startDate, end=endDate)
    return stockData

def makeGUI():
    global root
    root = tk.Tk()
    root.title("Stock Data Visualizer")
    root.geometry("1050x625")
    makeFirstPane(root)
    root.mainloop()

def plotData(data, stock):
    plt.clf()

    if len(data) < 20:
        data['Close'].plot()
        plt.title(f"Stock Price for  {stock} over the Last Year")
        plt.xlabel("Date")
        plt.ylabel("Stock Price in USD")

    else:
        data['Close'].plot()
        getBB(data)
        plt.axhline(y=BB_mean, color='r', linestyle='--')
        plt.axhline(y=BB_upper, color='g', linestyle='--')
        plt.axhline(y=BB_lower, color='g', linestyle='--')
        plt.title(f"Stock Price for  {stock} over the Last Year")
        plt.xlabel("Date")
        plt.ylabel("Stock Price in USD")
   
def getInput():
    input = stockSymbolEntry.get()
    if validStockSymbol(input):
        global stockSymbol
        stockSymbol = input
        makeSecondPane(root, daysAgoDate(365))
    else:
        print("Invalid stock symbol")

def threeDayButtonPress():
    makeSecondPane(root, daysAgoDate(3))

def oneWeekButtonPress():
    makeSecondPane(root, daysAgoDate(7))

def oneMonthButtonPress():
    makeSecondPane(root, daysAgoDate(30))
    
def threeYearButtonPress():
   makeSecondPane(root, daysAgoDate(1095))

def oneYearButtonPress():
   makeSecondPane(root, daysAgoDate(365))

def tenYearButtonPress():
    makeSecondPane(root, daysAgoDate(3650))

def makeSecondPane(root, endDate):
    clearScreen(root)
    createGUIHeader(root)
    stockData = getStockData(stockSymbol, endDate, getCurrentDate())

    SMA = getSMA(stockData)
    PERCENTAGE = priceChange(endDate, getCurrentDate())
    PE_RATIO = calculatePERatio(stockSymbol)

    button_frame = tk.Frame(root)
    threeDayButton = tk.Button(button_frame, text="3 DAY", font=("Arial", 15), command=lambda: threeDayButtonPress())
    threeDayButton.pack(side="left", padx=40, pady=10)
    oneWeekButton = tk.Button(button_frame, text="1 WEEK", font=("Arial", 15), command=lambda: oneWeekButtonPress())
    oneWeekButton.pack(side="left", pady= 10, padx=40)
    oneMonthButton = tk.Button(button_frame, text="1 MONTH", font=("Arial", 15), command=lambda: oneMonthButtonPress())
    oneMonthButton.pack(side="left", padx=40, pady=10)
    oneYearButton = tk.Button(button_frame, text="1 YEAR", font=("Arial", 15), command=lambda: oneYearButtonPress())
    oneYearButton.pack(side="left", padx=40, pady=10)
    threeYearButton = tk.Button(button_frame, text="3 YEARS", font=("Arial", 15), command=lambda: threeYearButtonPress())
    threeYearButton.pack(side="left",padx=40, pady=10)
    tenYearButton = tk.Button(button_frame, text="10 YEARS", font=("Arial", 15), command=lambda: tenYearButtonPress())
    tenYearButton.pack(side="left", padx=40, pady=10)
    button_frame.pack(side="top", fill="x")

    dataFrame = tk.Frame(root)
    SMA_label = tk.Label(dataFrame, text=f"Simple Moving Average (SMA): {SMA}", font=("Arial", 15))
    SMA_label.pack(side="left", padx=10, pady=10)
    EMA_label = tk.Label(dataFrame, text=f"Percentage change in price: {PERCENTAGE}", font=("Arial", 15))
    EMA_label.pack(side="left", padx=10, pady=10)
    PE_RATIO_label = tk.Label(dataFrame, text=f"Earnings per share: {PE_RATIO}", font=("Arial", 15))
    PE_RATIO_label.pack(side="left", padx=10, pady=10)
    dataFrame.pack(side="top", fill="x")

    plotData(stockData, stockSymbol)
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady= 25)

def makeFirstPane(root):
    clearScreen(root)
    createGUIHeader(root)
    global stockSymbolEntry
    introductionLabel = tk.Label(root, text="Welcome to the Stock Data Visualizer! Please enter a stock symbol to get started.", font=("Arial", 15))
    introductionLabel.pack(pady=10)

    stockSymbolEntry = tk.Entry(root, font=("Arial", 15))
    stockSymbolEntry.pack(pady=10)
    submitButton = tk.Button(root, text="Submit", font=("Arial", 15), command=lambda: getInput())
    submitButton.pack(pady=10)

def clearScreen(root):
    for widget in root.winfo_children():
        widget.destroy()

def createGUIHeader(root):
    clearScreen(root)
    createSeparationLine(root)
    header_frame = tk.Frame(root)
    header_frame.pack(side="top", fill="x")

    header_label = tk.Label(header_frame, text="Stock Data Visualizer, created by @BDaws04", font=("Arial", 24, "bold"))
    header_label.pack(pady=5)

    back_button= tk.Button(header_frame, text="BACK", font=("Arial", 15, "bold"), command=lambda: goBack(root))
    back_button.pack(side="right", padx=5, pady=5)
    createSeparationLine(root)    

def createSeparationLine(root):
    separation_line = tk.Frame(root, height=2, width=1000, bg="black")
    separation_line.pack()

#functions to get the dates for one day ago, three days ago, one week ago, one month ago, one year ago, and three years ago
def getCurrentDate():
    currentDateTime = datetime.datetime.now()
    currentDate = currentDateTime.date()
    return currentDate


def daysAgoDate(days):
    currentDateTime = datetime.datetime.now()
    return currentDateTime - datetime.timedelta(days=days)

def validStockSymbol(stockSymbol):
       try:
          stock_data = yf.Ticker(stockSymbol)
          history = stock_data.history(period='1d')
          return not history.empty
       except ValueError:
          return False

if __name__ == "__main__":
    main()
