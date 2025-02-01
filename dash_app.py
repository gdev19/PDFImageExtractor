import dash
from dash import Input, Output, html, dcc
from dash_extensions.enrich import (
    Output,
    Input,
    State,
    html,
    DashProxy,
    LogTransform,
    DashLogger,
    LogConfig,
    get_notification_log_writers,
)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                [
                    "Drag and Drop or ",
                    html.A(children="Select File"),
                ]
            ),
            style={
                "color": "silver",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "15px",
                "textAlign": "center",
                "padding": "5rem 0",
                "margin-bottom": "2rem",
                "margin-top": "10rem",
            },
        ),
        html.Div(
            [dcc.Dropdown(id="drop", options=[1, 2])],
        ),
        html.Div(id="container"),
    ]
)


# @app.callback(
#     Output("container", "children"), Input("drop", "value"), prevent_initial_call=True
# )
# def update(value):
#     if value == 1:
#         return html.Div("your layout for selection 1")
#     elif value == 2:
#         return html.Div("your layout for selection 2")
#     else:
#         html.Div("this should actually never show up")


@app.callback(
    [
    Output("container", "children")
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
    log=True,
)
def upload_file(content, filename):
    return html.Div(f"{filename}")


if __name__ == "__main__":
    app.run(debug=True, port=8051)
