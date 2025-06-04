import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import yfinance as yf
import pandas as pd
import numpy as np



def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

def get_ticker_price(ticker: str) -> dict:
    """
    return the price of ticker
    Args:
       ticker(str): The name of ticker
    Returns:
       dict: price 
    """
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        print(f"Successfully fetched price for {ticker}")
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have the price information for {ticker}."
            ),
        }

    current_price = info.get('regularMarketPrice')
    report = (
        f'The current price of {ticker} is {current_price}'
    )
    return {"status": "success", "report": report}



def get_dividend_information(ticker: str) -> dict:
    """
    Fetches dividend information for a given ticker.
    Args:
       ticker(str): The stock ticker symbol.
    Returns:
       dict: A dictionary containing dividend information.  Possible keys:
             "status": "success" or "error"
             "report":  A human-readable report (string) if status is "success"
             "error_message": An error message (string) if status is "error"
             "ex_dividend_date": The ex-dividend date (string, or None if not found)
             "dividend_rate": The dividend rate (float, or None if not found)
             "dividend_yield": The dividend yield (float, or None if not found)
             "payout_ratio": The payout ratio (float, or None if not found)
             "dividend_history": A pandas DataFrame containing the dividend history (if status is "success")
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # Extract dividend information
        ex_dividend_date = info.get('exDividendDate')
        if ex_dividend_date:
            # Convert timestamp to datetime string
            ex_dividend_date = pd.to_datetime(ex_dividend_date, unit='s').strftime('%Y-%m-%d')
        dividend_rate = info.get('dividendRate')
        dividend_yield = info.get('dividendYield')
        payout_ratio = info.get('payoutRatio')
        dividend_history = stock.dividends
        # Build report
        report_lines = []
        if ex_dividend_date:
            report_lines.append(f"Ex-Dividend Date: {ex_dividend_date}")
        else:
            report_lines.append("Ex-Dividend Date: Not found.")
        if dividend_rate:
            report_lines.append(f"Dividend Rate: {dividend_rate}")
        else:
            report_lines.append("Dividend Rate: Not found.")
        if dividend_yield:
            report_lines.append(f"Dividend Yield: {dividend_yield}%")  # Format as percentage
        else:
            report_lines.append("Dividend Yield: Not found.")
        if payout_ratio:
            report_lines.append(f"Payout Ratio: {payout_ratio}%")  # Format as percentage
        else:
            report_lines.append("Payout Ratio: Not found.")
        report = "\n".join(report_lines)
        print(f"Successfully fetched dividend information for {ticker}")
        return {
            "status": "success",
            "report": report,
        }
    except Exception as e:
        error_message = f"Error fetching dividend information for {ticker}: {e}"
        print(error_message)
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have dividend information for {ticker}. {e}" , # More descriptive error
        }



root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-lite",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time,get_ticker_price,get_dividend_information],
)
