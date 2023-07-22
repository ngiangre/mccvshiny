from shiny import App, reactive, render, ui
import shinyswatch
import mccv
from generate_data import generate_data_ui, generate_data_server
from mccv_results import mccv_results_ui, mccv_results_server

app_ui = ui.page_fluid(
    shinyswatch.theme.flatly(),
    ui.panel_title('Monte Carlo Cross Validation'),
    ui.navset_tab_card(
        ui.nav('MCCV',
            ui.markdown(
                '''
                Evidentiary and interpretable prediction. Learn more at [mccv.nickg.bio](mccv.nickg.bio).
                
                Use this app to simulate data, classify data into two groups, run MCCV, and inspect prediction results.
                '''),
            generate_data_ui('simulate'),
            mccv_results_ui('mccv_results')
            ),
        ui.nav_spacer(),
        ui.nav_control(
            ui.a("Github", href="https://github.com/ngiangre/mccvshiny", target="_blank")
        )
    )
)

def server(input, output, session):
    mccv_obj = mccv.mccv()
    generate_data_server('simulate',mccv_obj)
    mccv_results_server('mccv_results',mccv_obj)

app = App(app_ui, server)
