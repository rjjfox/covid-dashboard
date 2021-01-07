from coviddashboard import app
import json, plotly
from flask import render_template
from coviddashboard.analysis.uk_analysis import (
    pull_data,
    return_figures,
    get_current_numbers,
    compare_against_n_days_ago,
)


@app.route("/")
@app.route("/index")
def index():

    df = pull_data()
    figures = return_figures(df)
    current_cases, current_deaths = get_current_numbers(df)
    previous_week_cases, previous_week_deaths = compare_against_n_days_ago(7, df)
    previous_month_cases, previous_month_deaths = compare_against_n_days_ago(30, df)

    # plot ids for the html id tag
    ids = [f"figure-{i}" for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "index.html",
        ids=ids,
        figuresJSON=figuresJSON,
        current_cases=f"{current_cases:,.0f}",
        current_deaths=f"{current_deaths:,.0f}",
        previous_week_cases=f"{previous_week_cases:.2%}",
        previous_week_deaths=f"{previous_week_deaths:.2%}",
        previous_month_cases=f"{previous_month_cases:.2%}",
        previous_month_deaths=f"{previous_month_deaths:.2%}",
    )
