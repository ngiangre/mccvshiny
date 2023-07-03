from shiny import App, reactive, render, ui, module
from htmltools import css

@module.ui
def mccv_parameters_ui(label: str = 'mccv_parameters'):
    return ui.panel_sidebar(
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            ui.tags.div(
                ui.tags.br(),
                ui.input_slider("n", "Number of Bootstraps", 0, 200, 200),
                ui.input_checkbox_group(
                    'model_choices',
                    "Model",
                    ["Logistic Regression",
                    "Random Forest"]
                ),
                ui.output_ui('show_model')
            )
        )
@module.server
def mccv_parameters_server(input,output,session):
    @reactive.Calc
    def mccv_dictionary():
        mccv_dict = {}
        mccv_dict['N'] = input.n()
        mccv_dict['Models'] = input.model_choices()
        return mccv_dict
    @output
    @render.ui
    @reactive.event(input.run_model)
    def show_model():
        return str(mccv_dictionary())