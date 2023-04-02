import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Collect and preprocess data - simulating data collection from API
close_list = np.random.rand(30) * 100
print("Close List: ", close_list)

# Extract features - simulating feature extraction
X = []
for i in range(5, len(close_list)):
    x = []
    for j in range(5):
        x.append(close_list[i-j])
    X.append(x)
X = np.array(X)

# Generate labels - simulating label generation
y = []
for i in range(5, len(close_list)):
    if close_list[i] > np.mean(close_list[i-5:i]):
        y.append(1)
    else:
        y.append(0)

# Split the data - simulating train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model - using RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

pos_held = False

for i in range(5, len(close_list)):
    # Extract features for prediction - simulating feature extraction
    x = []
    for j in range(5):
        x.append(close_list[i-j])
    x = np.array(x).reshape(1, -1)

    # Make prediction - using the trained model
    pred = rf.predict(x)

    # Execute trade based on prediction - simulating trading execution
    if pred == 1 and not pos_held:
        print(f"Buy at {close_list[i]}")
        # Simulating buying the stock
        pos_held = True
    elif pred == 0 and pos_held:
        print(f"Sell at {close_list[i]}")
        # Simulating selling the stock
        pos_held = False
    else:
        print("No action taken")

# Simulating selling the stock at the end of the period
if pos_held:
    print(f"Sell at {close_list[-1]}")
    pos_held = False
