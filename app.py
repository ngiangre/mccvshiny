from shiny import App, reactive, render, ui
import shinyswatch
import mccv
from generate_data import generate_data_ui, generate_data_server
from mccv_parameters import mccv_parameters_ui, mccv_parameters_server

import pandas as pd

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
        sidebar = ui.panel_sidebar(
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            mccv_parameters_ui('mccv_parameters')
        ),
        main = ui.navset_tab_card(
                ui.nav('Tables',ui.output_data_frame('tables')),
                ui.nav('Plots',ui.output_ui('plots'))
            )
    )
)

def server(input, output, session):
    mccv_obj = mccv.mccv()
    generate_data_server('simulate',mccv_obj)
    mccv_parameters_server('mccv_parameters',mccv_obj)
    
    @reactive.Calc
    @reactive.event(input.run_model)
    def mccv_data():
        mccv_obj.run_mccv()
        return mccv_obj.mccv_data
            
    @output
    @render.data_frame
    @reactive.event(mccv_data)
    def tables():
        return render.DataGrid(
            mccv_data()['Performance'].groupby(['model','metric'])['value'].mean().reset_index()
        )

app = App(app_ui, server)
