from flask import Flask, request, Response, jsonify
from flask_cors import CORS
#from transformers import pipeline
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import ast
import numpy as np

app = Flask(__name__)
CORS(app)
global df
df = pd.read_excel("singstat_historical_shipping.xlsx").iloc[9:354]
df.columns = df.iloc[0]
df = df.iloc[1:]
df["Data Series"] = pd.to_datetime(df["Data Series"])
df.sort_values(by="Data Series", inplace=True)
df.reset_index(drop=True, inplace=True)
df.set_index("Data Series", inplace=True)


@app.route("/forecast-alive")
def is_alive():
    status_code = Response(status=200)
    return status_code

@app.route("/current_data", methods=["POST"])
def get_current():
    global df
    out = df.to_json(orient='index')
    return out

@app.route("/forecast", methods=["POST"])
def predict():
    args = request.get_json() 
    global df
    if "input" in args:
        input = args["input"]
        df_new = pd.read_json(ast.literal_eval(input), orient='index')
        df.reset_index(inplace=True)
        df = pd.concat([df, df_new])
        df.sort_values(by="Data Series", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.set_index("Data Series", inplace=True)
    order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)

    model = SARIMAX(np.asarray(df['Total Container Throughput '], dtype=float), order=order, seasonal_order=seasonal_order)
    results = model.fit()
    forecast_steps = 12  # Adjust as needed
    forecast = results.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(df.index[-1], periods=forecast_steps + 1, freq='M')[1:]
    forecast_df = pd.DataFrame(forecast.predicted_mean, index=forecast_index)

    out = forecast_df.to_json(orient='index')
    return out

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
