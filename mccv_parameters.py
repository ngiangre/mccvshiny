from shiny import App, reactive, render, ui, module
from htmltools import css

@module.ui
def mccv_parameters_ui(label: str = 'mccv_parameters'):
    return ui.panel_sidebar(
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            ui.tags.div(
                ui.tags.br(),
                ui.input_slider("n", "Number of Bootstraps", 0, 200, 200,step = 10,ticks=False),
                ui.input_checkbox_group(
                    'model_choices',
                    "Model(s)",
                    ["Logistic Regression",
                    "Random Forest"],
                    selected = ["Logistic Regression"]
                ),
                ui.input_slider("test_size", "Validation Set Proportion", 0.15, 0.85, 0.15, step=0.05, ticks=False)
            )
        )
@module.server
def mccv_parameters_server(input,output,session,mccv_obj):
    @reactive.Calc
    def mccv_dictionary():
        mccv_dict = {}
        mccv_dict['N'] = input.n()
        mccv_obj.num_bootstraps = mccv_dict['N']
        mccv_dict['Models'] = list(input.model_choices())
        mccv_obj.model_names = mccv_dict['Models']
        mccv_dict['Test Size'] = input.test_size()
        mccv_obj.test_size = mccv_dict['Test Size']
        return mccv_dict