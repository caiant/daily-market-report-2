# -*- coding: utf-8 -*-
"""market_report.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12vG3wjrwiMx2FfqUQlTJlKQlfaGKGXBE
"""


import yfinance as yf
import pandas as pd
import schedule
import time
import yagmail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz

# Email credentials
EMAIL_ADDRESS = "cailin.antonio@glccap.com"  # Replace with your email
EMAIL_PASSWORD = "ohdu zsxf lahi mpss"  # Use App Password if 2FA is enabled
TO_EMAIL = "caiantonio2427@gmail.com"  # Replace with recipient's email

# Define Yahoo Finance Tickers
tickers = {
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI",
    "SSE Composite": "000001.SS",
    "FTSE 100": "^FTSE",
    "DAX Index": "^GDAXI",
    "S&P 500 Futures": "^GSPC",
    "USD/JPY (Yen)": "JPY=X",
    "EUR/USD (Euro)": "EURUSD=X",
    "GBP/USD (Pound)": "GBPUSD=X",
    "Crude Oil (WTI)": "WTI",
    "UK 10Y Bond": "GB10Y.GB",
    "German 10Y Bond": "DE10Y.DE"
}

# Fetch market data
def get_market_data():
    data = []
    for name, symbol in tickers.items():
        try:
            asset = yf.Ticker(symbol)
            info = asset.history(period="1d")
            if not info.empty:
                last_close = info["Close"].iloc[-1]
                prev_close = info["Close"].iloc[-2] if len(info) > 1 else last_close
                change = last_close - prev_close
                percent_change = (change / prev_close) * 100

                data.append([name, last_close, change, f"{percent_change:.2f}%"])
        except Exception as e:
            data.append([name, "Error", "Error", "Error"])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Asset", "Last Price", "Change", "Change %"])
    return df

def format_html_table(df):
    table_style = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
    """
    
    table_html = df.to_html(index=False, escape=False)
    return table_style + table_html

    <head>
    <body>
        <h2> Daily Market Report - {date}</h2>
        <table>
            <tr>
                <th>Asset</th>
                <th>Last Price</th>
                <th>Change</th>
                <th>Change %</th>
            </tr>
    .format(date=datetime.now().strftime('%Y-%m-%d'))

    for _, row in df.iterrows():
        html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(*row)

    html += """
        </table>
    </body>
    </html>
    """
    return html

df = get_market_data()
html_table = format_html_table(df)
print(html_table)

from datetime import datetime

def send_email():
    df = get_market_data()
    report_html = format_html_table(df)

    # Email setup
    subject = f"Daily Market Report - {datetime.now().strftime('%Y-%m-%d')}"
    body = report_html  # HTML content

    try:
        # Initialize yagmail with your credentials
        yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send email
        yag.send(to=TO_EMAIL, subject=subject, contents=body)
        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

send_email()

