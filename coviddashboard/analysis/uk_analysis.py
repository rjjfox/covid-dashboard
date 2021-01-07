from requests import get
from urllib.parse import urlencode
from json import dumps
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt


def call_api(url):
    response = get(url, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f"Request failed: { response.text }")

    return response.json()


def pull_data():

    structure = {
        "date": "date",
        "newCases": "newCasesByPublishDate",
        "cumCases": "cumCasesByPublishDate",
        "newDeaths": "newDeaths28DaysByPublishDate",
        "cumDeaths": "cumDeaths28DaysByPublishDate",
    }

    api_params = {
        "filters": "areaType=overview",
        "structure": dumps(structure, separators=(",", ":")),
    }

    encoded_params = urlencode(api_params)

    endpoint = "https://api.coronavirus.data.gov.uk/v1/data?" + encoded_params

    data = call_api(endpoint)

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df.date)
    df = df.sort_values(by="date")
    df["7dayCases"] = df.newCases.rolling(window=7).mean()
    df["7dayDeaths"] = df.newDeaths.rolling(window=7).mean()
    df = df[df["date"] > "2020-03"]

    return df


def return_figures(df):

    graph = []
    graph.append(go.Bar(x=df.date.tolist(), y=df.newCases.tolist(), showlegend=False))
    graph.append(
        go.Scatter(
            x=df.date.tolist(),
            y=df["7dayCases"].tolist(),
            name="7 day moving average",
            showlegend=False,
        )
    )

    layout = dict(
        {
            "title": {
                "text": "Daily New Cases",
                # "yref": "container",
                # "y": 0.9,
                # "yanchor": "top",
                # "xanchor": "left",
                # "x": 0.1,
                "font": {"family": "Roboto", "size": 18},
                # "autosize": True,
            }
        }
    )

    figures = []
    figures.append(dict(data=graph, layout=layout))

    return figures


# def get_current_numbers(df):

#     current_7dayCases, current_7dayDeaths = df.loc[
#         df.date == df.date.max(), ["7dayCases", "7dayDeaths"]
#     ].values[0]

#     formatted_7dayCases = f"{current_7dayCases:,.0f}"
#     formatted_7dayDeaths = f"{current_7dayDeaths:,.0f}"

#     return formatted_7dayCases, formatted_7dayDeaths


def get_current_numbers(df):

    current_7dayCases, current_7dayDeaths = df.loc[
        df.date == df.date.max(), ["7dayCases", "7dayDeaths"]
    ].values[0]

    return current_7dayCases, current_7dayDeaths


def calculate_pct_difference(x, y):
    return x / y - 1


def compare_against_n_days_ago(n, df):

    current_7dayCases, current_7dayDeaths = get_current_numbers(df)

    comparison_date = df.date.max() - dt.timedelta(n)

    previous_7dayCases, previous_7dayDeaths = df.loc[
        df.date == comparison_date, ["7dayCases", "7dayDeaths"]
    ].values[0]

    cases_diff = calculate_pct_difference(current_7dayCases, previous_7dayCases)
    deaths_diff = calculate_pct_difference(current_7dayDeaths, previous_7dayDeaths)

    return cases_diff, deaths_diff
