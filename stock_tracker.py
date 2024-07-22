import matplotlib.pyplot as plt  # To create visualizations
import pandas as pd  # To handle and manipulate data
import requests  # To make HTTP requests to the API


def fetch_stock_data(symbol, api_key):
    # Construct the URL for the API request
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    # Make the HTTP request to the API
    response = requests.get(url)
    # Parse the JSON response
    data = response.json()
    # Return the JSON data
    return data


def parse_stock_data(data):
    if "Time Series (Daily)" not in data:
        print(
            "Error: Unable to retrieve data. Please check the stock symbol and API key."
        )
        return None
    time_series = data["Time Series (Daily)"]
    dates = []
    closing_prices = []
    opening_prices = []
    highest_prices = []
    lowest_prices = []
    volumes = []

    for date, daily_data in time_series.items():
        dates.append(date)
        closing_prices.append(float(daily_data["4. close"]))
        opening_prices.append(float(daily_data["1. open"]))
        highest_prices.append(float(daily_data["2. high"]))
        lowest_prices.append(float(daily_data["3. low"]))
        volumes.append(int(daily_data["5. volume"]))

    df = pd.DataFrame(
        {
            "Date": dates,
            "Close": closing_prices,
            "Open": opening_prices,
            "High": highest_prices,
            "Low": lowest_prices,
            "Volume": volumes,
        }
    )
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df


def plot_stock_data(df, symbol):
    # Check if DataFrame is None
    if df is None:
        return
    # Set the figure size for the plot
    plt.figure(figsize=(10, 5))
    # Plot the closing prices
    plt.plot(df["Date"], df["Close"], label=symbol)
    # Set the labels and title
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")  # Add "USD" to the y-axis label
    plt.title(f"Stock Prices for {symbol}")
    # Add a legend
    plt.legend()
    # Add a grid for better readability
    plt.grid(True)
    # Show the plot
    plt.show()


def save_to_csv(df, symbol):
    # Define the filename
    filename = f"{symbol}_stock_data.csv"
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main():
    # Get the stock symbol from the user
    stocks = {
        "Apple Inc.": "AAPL",
        "Microsoft Corporation": "MSFT",
        "Amazon.com Inc.": "AMZN",
        "Alphabet Inc. (Google)": "GOOGL",
        "Tesla Inc.": "TSLA",
        "NVIDIA": "NVD",
    }
    print("What Stock do you want to see?\n")
    for k, v in stocks.items():
        print(f"Possible Stocks can be {k}:{v} ")
    symbol = input("Enter the stock symbol: ")
    # Your Alpha Vantage API key
    api_key = "335MD1Y8H89WTQZ1"  # Replace with your actual API key
    # Fetch the stock data
    data = fetch_stock_data(symbol, api_key)
    # Parse the stock data
    df = parse_stock_data(data)
    # Plot the stock data
    plot_stock_data(df, symbol)
    # Ask the user if they want to save the data
    save_data = input("Do you want to save the data to a CSV file? (yes/no): ")
    if save_data.lower() == "yes":
        save_to_csv(df, symbol)


# Entry point of the script
if __name__ == "__main__":
    main()
