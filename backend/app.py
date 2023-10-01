from flask import Flask, request, Response, jsonify
from flask_cors import CORS
#from transformers import pipeline
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import ast
import numpy as np
from ncps.torch import LTC
import pytorch_lightning as pl
from ncps.wirings import AutoNCP
import torch

app = Flask(__name__)
CORS(app)
global df
df = pd.read_excel("singstat_historical_shipping.xlsx")
df["Data Series"] = pd.to_datetime(df["Data Series"])
df.sort_values(by="Data Series", inplace=True)
df.reset_index(drop=True, inplace=True)
df.set_index("Data Series", inplace=True)

global ltc_model
in_features = 4
out_features = 3
wiring = AutoNCP(100, out_features)  
ltc_model = LTC(in_features, wiring, batch_first=True)
ltc_model.load_state_dict(torch.load('model.pth'))
ltc_model.to("cpu")

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
    global out
    if "input" in args:
        input = args["input"]
        df_new = pd.read_json(ast.literal_eval(input), orient='index')
        df.reset_index(inplace=True)
        df = pd.concat([df, df_new])
        df.sort_values(by="Data Series", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.set_index("Data Series", inplace=True)

    # if "model" in args or "input" not in args:
    if ("model" in args and args["model"] == "SARIMAX") or ("model" not in args):
        order = (1, 1, 1)
        seasonal_order = (1, 1, 1, 12)

        model = SARIMAX(np.asarray(df['Total Container Throughput '], dtype=float), order=order, seasonal_order=seasonal_order)
        results = model.fit()
        forecast_steps = 12  # Adjust as needed
        forecast = results.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(df.index[-1], periods=forecast_steps + 1, freq='M')[1:]
        forecast_df = pd.DataFrame(forecast.predicted_mean, index=forecast_index)

        out = forecast_df.to_json(orient='index')
    else:
        global ltc_model
        
        ltc_model.eval()
        data = torch.tensor(df.iloc[-12:, :].loc[:, ["prevVA", "prevTC", "prevTCT", "gdp"]].values, dtype=torch.float32)/10000
        out = ltc_model(data)[0].detach().numpy() * 10000
        forecast_index = pd.date_range(df.index[-1], periods=12 + 1, freq='M')[1:]
        out = pd.DataFrame(out, columns=["prevVA", "prevTC", "prevTCT"], index=forecast_index)
        out.rename({"prevTCT":"0"}, inplace=True, axis=1)
        out = out.to_json(orient='index')
    return out

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
