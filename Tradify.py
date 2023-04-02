import alpaca_trade_api as tradeapi
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

#This code will only run with A premium purchase of Alpaca. To simulate its results use the MockBot file

# Define Alpaca API credentials
SEC_KEY = 'enter your secret key here'
PUB_KEY = 'enter yopur public key here'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

# Define stock symbol and position status
symb = "SPY"
pos_held = False

# Collect and preprocess data
market_data = api.get_bars(symb, 'minute', limit=50)
close_list = []
for bar in market_data[symb]:
    close_list.append(bar.c)
close_list = np.array(close_list, dtype=np.float64)

# Extract features
X = []
for i in range(5, len(close_list)):
    x = []
    for j in range(5):
        x.append(close_list[i-j])
    X.append(x)
X = np.array(X)

# Generate labels
y = []
for i in range(5, len(close_list)):
    if close_list[i] > np.mean(close_list[i-5:i]):
        y.append(1)
    else:
        y.append(0)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Run the trading loop
while True:
    # Collect data
    market_data = api.get_bars(symb, 'minute', limit=5)
    close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)
    close_list = np.array(close_list, dtype=np.float64)

    # Extract features for prediction
    x = []
    for j in range(5):
        x.append(close_list[j])
    x = np.array(x).reshape(1, -1)

    # Make prediction
    pred = rf.predict(x)

    # Execute trade based on prediction
    if pred == 1 and not pos_held:
        print("Buy")
        api.submit_order(
            symbol=symb,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        pos_held = True
    elif pred == 0 and pos_held:
        print("Sell")
        api.submit_order(
            symbol=symb,
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        pos_held = False
    
    time.sleep(60) # wait for 60 seconds before checking again

