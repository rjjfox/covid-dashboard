import pandas as pd
import plotly.graph_objects as go
from json import dumps
from requests import get
from urllib.parse import urlencode


def call_api(url):
    """Return response from API"""

    response = get(url, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f"Request failed: { response.text }")

    return response.json()


def get_vax_data():
    """Pull UK vaccination data from api"""

    structure = {
        "date": "date",
        "newFirst": "newPeopleVaccinatedFirstDoseByPublishDate",
        "cumFirst": "cumPeopleVaccinatedFirstDoseByPublishDate",
        "newSecond": "newPeopleVaccinatedSecondDoseByPublishDate",
        "cumSecond": "cumPeopleVaccinatedSecondDoseByPublishDate",
        "newThird": "newPeopleVaccinatedThirdInjectionByPublishDate",
        "cumThird": "cumPeopleVaccinatedThirdInjectionByPublishDate",
    }

    api_params = {
        "filters": "areaType=overview",
        "structure": dumps(structure, separators=(",", ":")),
    }

    # Encode params and call API
    encoded_params = urlencode(api_params)
    endpoint = "https://api.coronavirus.data.gov.uk/v1/data?" + encoded_params
    data = call_api(endpoint)

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df.date)
    df = df.fillna(0)
    df = df.sort_values("date", ascending=True)
    df["newTotal"] = df.newFirst + df.newSecond + df.newThird
    df["cumTotal"] = df.cumFirst + df.cumSecond + df.cumThird
    df["7dayFirstDose"] = df.newFirst.rolling(window=7).mean()
    df["7daySecondDose"] = df.newSecond.rolling(window=7).mean()
    df["7dayThirdDose"] = df.newThird.rolling(window=7).mean()
    df["7dayTotal"] = df.newTotal.rolling(window=7).mean()

    return df


def return_vax_figures(df):

    graph = []
    graph.append(
        go.Bar(
            x=df.date.tolist(),
            y=df.newFirst.tolist(),
            name="First Dose",
            hovertemplate="%{y:,.0f}",
        )
    )
    graph.append(
        go.Bar(
            x=df.date.tolist(),
            y=df.newSecond.tolist(),
            name="Second Dose",
            hovertemplate="%{y:,.0f}",
        )
    )
    graph.append(
        go.Bar(
            x=df.date.tolist(),
            y=df.newThird.tolist(),
            name="Third Dose",
            hovertemplate="%{y:,.0f}",
        )
    )
    graph.append(
        go.Scatter(
            x=df.date.tolist(),
            y=df["7dayTotal"].tolist(),
            name="7-day average",
            hovertemplate="%{y:,.0f}",
        )
    )

    layout = dict(
        {
            "title": {
                "text": "Daily Vaccinations in the UK",
                "font": {"family": "Roboto", "size": 18},
            },
            "margin": {
                "l": 40,
                "r": 20,
                "t": 65,
                "b": 40,
            },
            "hovermode": "x unified",
            "hoverlabel": {
                "bgcolor": "white",
                "font_size": 16,
                "font_family": "Roboto",
            },
            "legend": {
                "yanchor": "top",
                "y": 0.95,
                "xanchor": "left",
                "x": 0.05,
                "bgcolor": "#F9F9FC",
            },
            "barmode": "stack",
        }
    )

    figures = []
    figures.append(dict(data=graph, layout=layout))

    return figures


def get_current_vaccinations(df):

    firstDoseTotal, secondDoseTotal, thirdDoseTotal, rate = df.loc[
        df.date == df.date.max(),
        [
            "cumFirst",
            "cumSecond",
            "cumThird",
            "7dayTotal",
        ],
    ].values[0]

    return firstDoseTotal, secondDoseTotal, thirdDoseTotal, rate
