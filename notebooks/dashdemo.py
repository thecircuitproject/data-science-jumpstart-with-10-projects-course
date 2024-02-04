import dash
from dash import dcc, html, Dash, Input, Output
import numpy as np
import pandas as pd
import plotly
import plotly.express as px

pd.options.plotting.backend = "plotly"


def tweak_alta(df):
    return (
        df.assign(DATE=pd.to_datetime(df.DATE).dt.tz_localize("America/Denver"))
        .loc[
            :,
            [
                "DATE",
                "STATION",
                "NAME",
                "LATITUDE",
                "LONGITUDE",
                "PRCP",
                "SNOW",
                "SNWD",
                "TMIN",
                "TMAX",
                "TOBS",
            ],
        ]
        .assign(
            MONTH=lambda df_: df_.DATE.dt.month,
            YEAR=lambda df_: df_.DATE.dt.year,
            SEASON=lambda df_: np.select(
                [df_.MONTH < 5, df_.MONTH > 10],
                [
                    (df_.YEAR - 1).astype(str)
                    + "-"
                    + (df_.YEAR).astype(str)
                    + " Season",
                    (df_.YEAR).astype(str)
                    + "-"
                    + (df_.YEAR + 1).astype(str)
                    + " Season",
                ],
                default="Off Season",
            ),
        )
    )


df = pd.read_csv(
    "notebooks/data/snow-alta-1990-2017.csv"
)
alta = tweak_alta(df)
app = Dash(__name__)
fig = alta.query('SEASON.str.contains("2010-2011")').plot(
    x="DATE", y="SNWD", title="2011 Season Snow Depth"
)
app.layout = dash.html.Div(
    children=[
        dash.html.H1("Alta 2011 Season"),
        dash.dcc.Markdown(
            """## Line Plot of Snow Depth

* This is Markdown text.
* Plot of Snow Depth

    """
        ),
        dash.dcc.Graph(id="line-graph", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
