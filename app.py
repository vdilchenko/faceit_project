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


def window_mean():
    series = []
    def averager(kills, deaths):
        series.append(kills / deaths)
        total = sum(series)
        return total / len(series)
    return averager


def create_plot(stats):
    averager = window_mean()
    data = [
        go.Scatter(
            x=[x for x in range(len(stats['Kills']))],
            y=[kills/deaths for kills, deaths in zip(stats['Kills'][::-1], stats['Deaths'][::-1])],
            hovertext='KD',
            name='KD per match'
        ),
        go.Scatter(
            x=[x for x in range(len(stats['Kills']))],
            y=[averager(k, d) for k, d in zip(stats['Kills'], stats['Deaths'])],
            hovertext='KD',
            name='AVG KD'
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == "__main__":
    app.run()
