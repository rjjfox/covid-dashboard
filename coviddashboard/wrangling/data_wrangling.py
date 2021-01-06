from requests import get
from urllib.parse import urlencode
from json import dumps
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly


def get_data(url):
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

    data = get_data(endpoint)

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df.date)
    df = df.sort_values(by="date")
    df["7dayCases"] = df.newCases.rolling(window=7).mean()
    df["7dayDeaths"] = df.newDeaths.rolling(window=7).mean()
    df = df[df["date"] > "2020-03"]

    return df


def return_figures():

    df = pull_data()

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


def get_current_moving_average():

    df = pull_data()

    current_moving_average = df.loc[df.date == df.date.max(), "7dayCases"][0].astype(
        "int"
    )

    formatted = f"{current_moving_average:,}"

    return formatted
