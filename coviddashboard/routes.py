from coviddashboard import app
import json, plotly
from flask import render_template
from coviddashboard.analysis.country_analysis import (
    get_uk_data,
    get_france_data,
    return_figures,
    get_current_numbers,
    compare_against_n_days_ago,
)


@app.route("/")
@app.route("/index")
def index():

    uk_df = get_uk_data()
    fr_df = get_france_data()

    figures = return_figures(uk_df)
    figures = figures + return_figures(fr_df)

    uk_current_cases, uk_current_deaths = get_current_numbers(uk_df)
    uk_previous_week_cases, uk_previous_week_deaths = compare_against_n_days_ago(
        7, uk_df
    )
    uk_previous_month_cases, uk_previous_month_deaths = compare_against_n_days_ago(
        30, uk_df
    )

    fr_current_cases, fr_current_deaths = get_current_numbers(fr_df)
    fr_previous_week_cases, fr_previous_week_deaths = compare_against_n_days_ago(
        7, fr_df
    )
    fr_previous_month_cases, fr_previous_month_deaths = compare_against_n_days_ago(
        30, fr_df
    )

    # plot ids for the html id tag
    ids = [f"figure-{i}" for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "index.html",
        ids=ids,
        figuresJSON=figuresJSON,
        uk_current_cases=f"{uk_current_cases:,.0f}",
        uk_current_deaths=f"{uk_current_deaths:,.0f}",
        uk_previous_week_cases=f"{uk_previous_week_cases:.0%}",
        uk_previous_week_deaths=f"{uk_previous_week_deaths:.0%}",
        uk_previous_month_cases=f"{uk_previous_month_cases:.0%}",
        uk_previous_month_deaths=f"{uk_previous_month_deaths:.0%}",
        fr_current_cases=f"{fr_current_cases:,.0f}",
        fr_current_deaths=f"{fr_current_deaths:,.0f}",
        fr_previous_week_cases=f"{fr_previous_week_cases:.0%}",
        fr_previous_week_deaths=f"{fr_previous_week_deaths:.0%}",
        fr_previous_month_cases=f"{fr_previous_month_cases:.0%}",
        fr_previous_month_deaths=f"{fr_previous_month_deaths:.0%}",
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/data")
def data():
    return render_template("data.html")