from shiny import App, reactive, render, ui
import shinyswatch
import mccv

app_ui = ui.page_fluid(
    shinyswatch.theme.flatly(),
    ui.panel_title('Monte Carlo Cross Validation'),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.output_ui('upload_data'),
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            ui.tags.div(
                ui.tags.br(),
                ui.input_slider("n", "Number of Bootstraps", 0, 200, 200),
                ui.input_checkbox_group(
                    'model_choices',
                    "Model",
                    ["Logistic Regression",
                    "Random Forest"]
                )
            )
        ),
        ui.navset_tab_card(
            ui.nav('Tables',ui.output_ui('show_model')),
            ui.nav('Plots',ui.output_ui('plots'))
        )
    )
)


def server(input, output, session):
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
