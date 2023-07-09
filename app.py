from shiny import App, reactive, render, ui
import shinyswatch
import mccv
from generate_data import generate_data_ui, generate_data_server
from mccv_parameters import mccv_parameters_ui, mccv_parameters_server

app_ui = ui.page_fluid(
    shinyswatch.theme.flatly(),
    ui.panel_title('Monte Carlo Cross Validation'),
    ui.markdown(
        '''
        Evidentiary and interpretable prediction. Learn more at [mccv.nickg.bio](mccv.nickg.bio).
        
        Use this app to simulate data, classify data into two groups, run MCCV, and inspect prediction results.
        '''),
    generate_data_ui('simulate'),
    ui.layout_sidebar(
        sidebar = mccv_parameters_ui('mccv_parameters'),
        main = ui.navset_tab_card(
            ui.nav('Tables',ui.output_ui('tables')),
            ui.nav('Plots',ui.output_ui('plots'))
        )
    )
)

def server(input, output, session):
    mccv_obj = mccv.mccv()
    generate_data_server('simulate',mccv_obj)
    mccv_parameters_server('mccv_parameters',mccv_obj)
    
    @output
    @render.ui
    def tables():
        return ui.div(
            render.data_frame(mccv)
        )

app = App(app_ui, server)
