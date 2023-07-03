from shiny import App, reactive, render, ui
import shinyswatch
import mccv
from generate_data import generate_data_ui, generate_data_server

app_ui = ui.page_fluid(
    shinyswatch.theme.flatly(),
    ui.panel_title('Monte Carlo Cross Validation'),
    generate_data_ui('simulate'),
    ui.layout_sidebar(
        ui.panel_sidebar(
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
        ),
        ui.navset_tab_card(
            ui.nav('Tables',ui.output_ui('tables')),
            ui.nav('Plots',ui.output_ui('plots'))
        )
    )
)

def server(input, output, session):
    generate_data_server('simulate')
    
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

app = App(app_ui, server)
