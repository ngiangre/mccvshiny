from shiny import App, reactive, render, ui, module
from htmltools import css

import os

@module.ui
def mccv_parameters_ui(label: str = 'mccv_parameters'):
    return ui.tags.div(
                ui.tags.br(),
                ui.input_slider("n", "Number of Bootstraps", 0, 200, 200,step = 10,ticks=False),
                ui.input_slider("n_jobs", "Number of Jobs", 
                                min=1, 
                                max=os.cpu_count(),
                                value=1,
                                step = 1,
                                ticks=False),
                ui.input_checkbox_group(
                    'model_choices',
                    "Model:",
                    ["Logistic Regression"],
                    selected = ["Logistic Regression"]
                ),
                ui.input_slider("test_size", "Validation Set Proportion", 0.15, 0.85, 0.15, step=0.05, ticks=False),
                ui.output_text_verbatim('tmp')
            )
@module.server
def mccv_parameters_server(input,output,session,mccv_obj):
    @reactive.Effect
    def _():
        mccv_obj.num_bootstraps = input.n()
        mccv_obj.n_jobs = input.n_jobs()
        mccv_obj.model_names = input.model_choices()
        mccv_obj.test_size = input.test_size()