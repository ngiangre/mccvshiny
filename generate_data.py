from shiny import App, reactive, render, ui, module
from htmltools import css

@module.ui
def generate_data_ui(label: str = "simulate"):
    return     ui.panel_main(
        {"style": "border: 1px solid #ccc; border-radius: 5px; margin: 5px 0;"},
        ui.h2('Generate Univariate Data'),
        ui.div(
            ui.input_selectize('dist','Distribution Type',choices = ['Normal','T','Beta'],multiple=False,width = '200px'),
            ui.output_ui('dist_params'),
            style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
            )
        )
    )

@module.server
def generate_data_server(input, output, session):
    
    @output
    @render.ui
    def dist_params():
        return 'Placeholder'
