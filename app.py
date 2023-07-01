from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.row(ui.h1('Monte Carlo Cross Validation')),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.output_ui('upload_data'),
            ui.input_action_button('run_model','Run MCCV'),
            ui.output_ui('parameterize_model')
        ),
        ui.panel_main(
            ui.output_ui('show_model')
        )
    )
)


def server(input, output, session):
    @output
    @render.ui
    def parameterize_model():
        ui.input_slider("n", "N", 0, 100, 20)
        
    @output
    @render.ui
    def show_model():
        return 'model run'


app = App(app_ui, server)
