
import csv
import yfinance as yf

# Function to get a positive number
def get_positive_number(message):
    while True:
        try:
            value = float(input(message))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input! Enter a valid number.")


# Function to fetch the latest stock price
def get_stock_price(symbol):

    stock = yf.Ticker(symbol)

    # First try to get the latest intraday price
    history = stock.history(
        period="1d",
        interval="1m"
    )

    price_type = "Latest intraday price"

    # If intraday data is unavailable, use daily data
    if history.empty:
        history = stock.history(
            period="5d",
            interval="1d"
        )
        price_type = "Latest available daily close"

    if history.empty or "Close" not in history.columns:
        raise ValueError("Stock price not available.")

    prices = history["Close"].dropna()

    if prices.empty:
        raise ValueError("No valid price found.")

    current_price = float(prices.iloc[-1])
    price_date = str(prices.index[-1])

    return current_price, price_date, price_type


# Main program
def main():

    print("=" * 50)
    print("     STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 50)

    portfolio = []

    while True:

        symbol = input("\nEnter stock ticker (example AAPL): ").strip().upper()

        if not symbol:
            print("Ticker cannot be empty.")
            continue

        buy_price = get_positive_number("Enter buying price: ")
        quantity = get_positive_number("Enter share quantity: ")

        print("\nFetching latest stock price...")

        try:
            current_price, price_date, price_type = get_stock_price(symbol)

            invested = buy_price * quantity
            current_value = current_price * quantity

            gain_loss = current_value - invested
            percentage = (gain_loss / invested) * 100

            holding = {
                "Ticker": symbol,
                "Buy Price": round(buy_price, 2),
                "Quantity": quantity,
                "Current Price": round(current_price, 2),
                "Total Invested": round(invested, 2),
                "Current Value": round(current_value, 2),
                "Gain/Loss": round(gain_loss, 2),
                "Gain/Loss (%)": round(percentage, 2),
                "Price Date": price_date,
                "Price Type": price_type
            }

            portfolio.append(holding)

            print("\nStock added successfully!")
            print("Current Price:", round(current_price, 2))
            print("Total Invested:", round(invested, 2))
            print("Current Value:", round(current_value, 2))
            print("Gain/Loss:", round(gain_loss, 2))
            print("Gain/Loss Percentage:", round(percentage, 2), "%")

        except Exception as error:
            print("\nUnable to fetch stock data.")
            print("Reason:", error)
            print("Check your internet connection and ticker symbol.")

        again = input("\nAdd another stock? (y/n): ").strip().lower()

        if again not in ("y", "yes"):
            break

    # Save portfolio data into CSV file
    if portfolio:

        filename = "portfolio_summary.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=portfolio[0].keys()
            )

            writer.writeheader()
            writer.writerows(portfolio)

        # Display final portfolio summary
        print("\n" + "=" * 50)
        print("           FINAL PORTFOLIO SUMMARY")
        print("=" * 50)

        for stock in portfolio:
            print(
                f"{stock['Ticker']}: "
                f"Invested = {stock['Total Invested']:.2f}, "
                f"Current Value = {stock['Current Value']:.2f}, "
                f"Gain/Loss = {stock['Gain/Loss']:.2f} "
                f"({stock['Gain/Loss (%)']:.2f}%)"
            )

        print("\nPortfolio saved successfully!")
        print("File generated:", filename)

    else:
        print("\nNo stock data was added.")


# Run the program
if __name__ == "__main__":
    main()
