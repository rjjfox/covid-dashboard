from coviddashboard import app
import json, plotly
from flask import render_template
from coviddashboard.wrangling.data_wrangling import (
    return_figures,
    get_current_moving_average,
)


@app.route("/")
@app.route("/index")
def index():

    figures = return_figures()
    current_moving_average = get_current_moving_average()

    # plot ids for the html id tag
    ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "index.html",
        ids=ids,
        figuresJSON=figuresJSON,
        current_moving_average=current_moving_average,
    )
