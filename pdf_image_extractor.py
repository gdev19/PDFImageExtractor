import base64
import io
from pathlib import Path
from urllib.parse import quote
from dash import Dash, dcc
from dash_extensions.enrich import (
    Input,
    Output,
    State,
    html,
)
from pypdf import PdfReader
from pathvalidate import sanitize_filepath, ValidationError

from flask_instance import server

if __name__ == "__main__":
    URL_BASE_PATHNAME = None
else:
    URL_BASE_PATHNAME = "/apps/pdf_img_extractor/"

STATIC_DIR = "static/"
APP_NAME = "pdf_img_extractor"

style = {
    "image": {
        "width": "200px",  # Relative width
        "height": "150px",  # Relative height
        "margin": "30px",  # Relative margin
        "border-radius": "15px",  # Rounded corners
        "border-style": "solid",  # Add border
        "border-color": "grey",  # Set border color
        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",  # Add shadow effect
        "transition": "transform 0.5s",  # Add transition effect
    },
    "text_title": {
        "margin": "30px",  # Relative margin
        "font-family": "Arial, sans-serif",  # Specify font family
        "font-size": "30px",  # Set font size
        "color": "#333",  # Set text color
        "text-align": "center",
        "display": "flex",
        "justify-content": "center",
        "flex-wrap": "wrap",
    },
    "text_info": {
        # "margin": "30px",  # Relative margin
        "font-family": "Arial, sans-serif",  # Specify font family
        "font-size": "20px",  # Set font size
        "color": "#333",  # Set text color
        "text-align": "center",
        "display": "flex",
        "justify-content": "center",
        "flex-wrap": "wrap",
    },
    "image_name": {
        "font-family": "Arial, sans-serif",  # Custom font family
        "font-size": "18px",  # Font size
        "color": "#333",  # Text color
    }
}
app = Dash(__name__, server=server, url_base_pathname=URL_BASE_PATHNAME)
app.title = "PDF Image Extractor"
app.layout = html.Div(
    [
        html.H1(
            "PDF Image Extractor - Upload a PDF file to extract images",
            style=style["text_title"],
        ),
        html.P(
            "Don't close the tab until you download the images.",
            style=style["text_info"],
        ),
        html.P(
            "The size of the input PDF file should be less than 50 MB.",
            style=style["text_info"],
        ),
        html.P(
            "We clean up the images every hour from the server.",
            style=style["text_info"],
        ),
        dcc.Upload(
            id="upload-data",
            max_size=50 * 1024 * 1024,  # 50 MB
            multiple=False,
            accept="application/pdf",
            children=html.Div(
                [
                    "Drag and Drop or ",
                    html.A(children="Select File"),
                ]
            ),
            style={
                "color": "black",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "15px",
                "textAlign": "center",
                "padding": "5rem 0",
                "margin": "2rem",
                "margin-top": "2rem",
            },
        ),
        html.Div(id="container"),
    ]
)


def get_safe_path(user_input_path: str) -> Path:
    try:
        # Sanitize the input path for cross-platform safety
        safe_path = sanitize_filepath(user_input_path, platform="auto")
        return Path(safe_path)
    except ValidationError as e:
        print("Invalid path provided:", e)
        return None


@app.callback(
    Output("container", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
)
def upload_file(content, filename):
    _, content_string = content.split(",")
    decoded = base64.b64decode(content_string)
    reader = PdfReader(io.BytesIO(decoded))
    image_urls = []
    for page_number, page in enumerate(reader.pages):
        for count, image_file_object in enumerate(page.images):
            output_folder = Path(STATIC_DIR) / Path(APP_NAME) / Path(filename).stem
            safe_path = get_safe_path(output_folder)
            if safe_path is None:
                return html.Div("Invalid PDF filename provided")
            safe_path.mkdir(parents=True, exist_ok=True)
            image_filename = f"{page_number}_{count}_{image_file_object.name}"
            image_path = output_folder / image_filename
            with open(image_path, "wb") as fp:
                fp.write(image_file_object.data)
            image_urls.append(Path(APP_NAME) / Path(filename).stem / image_filename)
    return [
        html.A(
            [
                html.Img(src=quote(f"/static/{image_url}"), style=style["image"]),
            ],
            href=quote(f"/static/{image_url}"),
            target="_blank",
            title=image_url.name,
        )
        for image_url in image_urls
    ]


if __name__ == "__main__":
    app.run(port=8051)
