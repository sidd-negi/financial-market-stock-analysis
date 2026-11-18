"""A small Linear Regression example for stock price estimation."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def make_prediction(data):
    """Train on earlier observations, test on later observations, then estimate next price."""
    prices = data["close"].to_numpy()
    number_of_previous_days = 5

    features = []
    targets = []

    for position in range(number_of_previous_days, len(prices)):
        features.append(prices[position - number_of_previous_days:position])
        targets.append(prices[position])

    features = np.asarray(features)
    targets = np.asarray(targets)

    # Keep the order of time: earlier records train the model, later records test it.
    split_point = int(len(features) * 0.8)
    x_train = features[:split_point]
    x_test = features[split_point:]
    y_train = targets[:split_point]
    y_test = targets[split_point:]

    model = LinearRegression()
    model.fit(x_train, y_train)

    test_predictions = model.predict(x_test)
    next_days = prices[-number_of_previous_days:].reshape(1, -1)
    next_price = model.predict(next_days)[0]

    return {
        "next_price": float(next_price),
        "mae": float(mean_absolute_error(y_test, test_predictions)),
        "r2": float(r2_score(y_test, test_predictions))
    }
