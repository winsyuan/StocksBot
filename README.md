## Stonks Bot

### What It Does:

- discord bot that helps user retrieve more data on stocks quickly
    - company information
    - stock prices
    - stock analytics
    - trending stocks

### Technology Used:
- python
- Utilized Packages
  - python.py
  - yfinace
  - mplfinance 
  - beautifulsoup   


### Run Locally

1) Clone the repo
2) Create a virtual environment  
    ```python -m venv venv```
3) Activate the virtual environment  
    ```venv\Scripts\activate``` On Windows  
    ```source venv/bin/active``` On macOS  
4) Install Dependencies  
    ```pip install -r requirements.txt```
5) Run  
    ```python main.py```


### Commands

**Shows stock price analytics**  
`$graph [StockName] [YYYY-MM-DD: start date] [(YYYY-MM-DD): end date] [1m/1h/1d/1wk/1mo: interval]`

**Shows top active stocks traded**  
`$active`

**Shows the amount of stocks you can buy**  
`$buy [StockName] [AmountOfMoney]`

**Shows more detail for a stock**  
`$ticket [StockName]`

**Outputs all commands available**  
`$help`

