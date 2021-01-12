# COVID-19 Dashboard

A data dashboard giving a snapshot of the COVID-19 situation in the UK and France. Built with Python using Flask and Plotly and hosted on Heroku as a web app. See it live [here](https://covid-dashboard-rfox.herokuapp.com/).

## Table of Contents

- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Built With](#built-with)
- [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need Python v3.6 or later on your local machine.

### Installing

Clone/fork the repo onto your local machine.

It is then recommended to use a virtual environment to install the dependencies using the `requirements.txt` file.

```cli
pip install -r requirements.txt
```

With these installed, you simply need to run

```cli
flask run
```

We have defined a `.flaskenv` file to hold flask environment variables which Flask knows to look for since we installed the `python-dotenv` package with the `requirements.txt`.

After running `flask run`, you will be given a local address to see the web app live.

## Deployment

I utilised Heroku's free tier to host the web app. To do the same, create a project on Heroku's website and then I recommend linking the project to a Github repository in the Deploy section.

Alternatively, you can use the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). Provided you have already created a project on the site, use

```cli
heroku git:remote -a [project-name]
git push heroku master
```

Use the same project name as the one you created. If successful, you can then go to `https://[project-name].herokuapp.com/`.

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web application framework used
- [Plotly](https://plotly.com/python/) - For data vizualisation
- [UK Government COVID-19 API](https://coronavirus.data.gov.uk/details/developers-guide) - For UK data
- [WHO Data](https://covid19.who.int/) - For France data
- [Heroku](https://heroku.com/) - Cloud platform used for deployment

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
