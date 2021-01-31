import pandas as pd
import plotly.graph_objects as go


def get_vax_data():
    """Pull UK vaccination data from api"""

    df = pd.read_csv(
        "https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumPeopleVaccinatedFirstDoseByPublishDate&metric=cumPeopleVaccinatedSecondDoseByPublishDate&metric=newPeopleVaccinatedFirstDoseByPublishDate&metric=newPeopleVaccinatedSecondDoseByPublishDate&format=csv"
    )

    df["date"] = pd.to_datetime(df.date)
    df["cumTotal"] = (
        df.cumPeopleVaccinatedFirstDoseByPublishDate
        + df.cumPeopleVaccinatedSecondDoseByPublishDate
    )
    df["newTotal"] = (
        df.newPeopleVaccinatedFirstDoseByPublishDate
        + df.newPeopleVaccinatedSecondDoseByPublishDate
    )
    df = df.sort_values("date", ascending=True)
    df["7dayFirstDose"] = df.newPeopleVaccinatedFirstDoseByPublishDate.rolling(
        window=7
    ).mean()
    df["7daySecondDose"] = df.newPeopleVaccinatedSecondDoseByPublishDate.rolling(
        window=7
    ).mean()
    df["7dayTotal"] = df.newTotal.rolling(window=7).mean()

    return df


def return_vax_figures(df):

    graph = []
    graph.append(
        go.Bar(
            x=df.date.tolist(),
            y=df.newPeopleVaccinatedFirstDoseByPublishDate.tolist(),
            name="First Dose",
            hovertemplate="%{y:,.0f}",
        )
    )
    graph.append(
        go.Bar(
            x=df.date.tolist(),
            y=df.newPeopleVaccinatedSecondDoseByPublishDate.tolist(),
            name="Second Dose",
            hovertemplate="%{y:,.0f}",
        )
    )
    graph.append(
        go.Scatter(
            x=df.date.tolist(),
            y=df["7dayTotal"].tolist(),
            name="7 day moving average",
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

    firstDoseTotal, secondDoseTotal, rate = df.loc[
        df.date == df.date.max(),
        [
            "cumPeopleVaccinatedFirstDoseByPublishDate",
            "cumPeopleVaccinatedSecondDoseByPublishDate",
            "7dayTotal",
        ],
    ].values[0]

    return firstDoseTotal, secondDoseTotal, rate