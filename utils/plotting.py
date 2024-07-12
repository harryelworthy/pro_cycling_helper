import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
from pathlib import Path
from IPython.display import display, HTML
import numpy as np
import matplotlib.pyplot as plt
from plotnine import ggplot, geom_point, aes, labs
import pandas as pd


def plot_3D_projection_html(
    ### In VS Code IPython.display.HTML will not work, so you will need to save the HTML snippet to a file and open it in a browser
    labels: np.ndarray,
    projections: np.ndarray,
    image_paths: np.ndarray,
    image_data_uris: Dict[str, str],
    show_legend: bool = False,
    show_markers_with_text: bool = True
) -> None:
    # Create a separate trace for each unique label
    unique_labels = np.unique(labels)
    traces = []
    for unique_label in unique_labels:
        mask = labels == unique_label
        customdata_masked = image_paths[mask]
        trace = go.Scatter3d(
            x=projections[mask][:, 0],
            y=projections[mask][:, 1],
            z=projections[mask][:, 2],
            mode='markers+text' if show_markers_with_text else 'markers',
            text=labels[mask],
            customdata=customdata_masked,
            name=str(unique_label),
            marker=dict(size=8),
            hovertemplate="<b>class: %{text}</b><br>path: %{customdata}<extra></extra>"
        )
        traces.append(trace)

    # Create the 3D scatter plot
    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        width=1000,
        height=1000,
        showlegend=show_legend
    )

    # Convert the chart to an HTML div string and add an ID to the div
    plotly_div = fig.to_html(full_html=False, include_plotlyjs=False, div_id="scatter-plot-3d")

    # Define your JavaScript code for copying text on point click
    javascript_code = f"""
    <script>
        function displayImage(imagePath) {{
            var imageElement = document.getElementById('image-display');
            var placeholderText = document.getElementById('placeholder-text');
            var imageDataURIs = {image_data_uris};
            imageElement.src = imageDataURIs[imagePath];
            imageElement.style.display = 'block';
            placeholderText.style.display = 'none';
        }}

        // Get the Plotly chart element by its ID
        var chartElement = document.getElementById('scatter-plot-3d');

        // Add a click event listener to the chart element
        chartElement.on('plotly_click', function(data) {{
            var customdata = data.points[0].customdata;
            displayImage(customdata);
        }});
    </script>
    """

    # Create an HTML template including the chart div and JavaScript code
    html_template = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                #image-container {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 200px;
                    height: 200px;
                    padding: 5px;
                    border: 1px solid #ccc;
                    background-color: white;
                    z-index: 1000;
                    box-sizing: border-box;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                }}
                #image-display {{
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                }}
            </style>
        </head>
        <body>
            {plotly_div}
            <div id="image-container">
                <img id="image-display" src="" alt="Selected image" style="display: none;" />
                <p id="placeholder-text">Click on a data entry to display an image</p>
            </div>
            {javascript_code}
        </body>
    </html>
    """

    # Display the HTML template in the Jupyter Notebook
    return(html_template)


def plot_2D_projection(
    labels: np.ndarray,
    projections: np.ndarray,
    show_legend: bool = True,
    title_end = ""
) -> None:
    # Create a scatter plot
    plt.figure(figsize=(10, 6))

    # Plot each point with a different color based on the label
    for label in np.unique(labels):
        idx = labels == label
        plt.scatter(projections[idx, 0], projections[idx, 1], label=f'Label {label}')

    # Add title and labels
    plt.title(f'2D Projections with Labeled Teams{title_end}')
    if show_legend:
        # Add the legend outside the plot area
        plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
        # Adjust the plot to make room for the legend
        plt.subplots_adjust(right=0.75)

    plt.grid(False)
    return(plt.show())

def plot_2D_projection_plotnine(
    labels: np.ndarray,
    projections: np.ndarray,
    show_legend: bool = True,
    title_end = ""
) -> None:
    # Create a DataFrame from the data
    df = pd.DataFrame({
        'Projection1': projections[:, 0],
        'Projection2': projections[:, 1],
        'Label': labels
    })

    # Create the plot
    plot = (ggplot(df, aes(x='Projection1', y='Projection2', color='factor(Label)'))
            + geom_point(size=5)
            + labs(title='2D Projections with Labels', color='Label')
            )

    # Display the plot
    return(plot)
