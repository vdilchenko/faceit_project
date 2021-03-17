from flask import Flask, render_template, request, redirect
import plotly
import plotly.graph_objs as go
from faceit_stats import get_stats
import json


app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def post_form():
    if request.method == "POST":
        nickname = request.form['nickname']
        limit = request.form['limit'] if request.form['limit'] is not None else 20
        stats = get_stats(nickname, limit)
        bar = create_plot(stats)
        return render_template("index.html", plot=bar)
    return render_template("index.html")


def accum_kd(stats):
    kd = 0
    count = 1
    all_kd = []
    for kills, deaths in zip(stats['Kills'][::-1], stats['Deaths'][::-1]):
        kd += kills/deaths
        all_kd.append(kd / count)
        count += 1
    return all_kd


def create_plot(stats):
    data = [
        go.Scatter(
            x=[x for x in range(len(stats['Kills']))],
            y=[kills/deaths for kills, deaths in zip(stats['Kills'][::-1], stats['Deaths'][::-1])],
            hovertext='KD',
            name='KD per match'
        ),
        go.Scatter(
            x=[x for x in range(len(stats['Kills']))],
            y=accum_kd(stats),
            hovertext='KD',
            name='AVG KD'
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
