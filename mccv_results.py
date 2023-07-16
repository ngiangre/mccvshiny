from shiny import App, reactive, render, ui, module
from htmltools import css

from mccv_parameters import mccv_parameters_ui, mccv_parameters_server

@module.ui
def mccv_results_ui(label: str = 'mccv_parameters'):
    return ui.layout_sidebar(
        sidebar = ui.panel_sidebar(
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            mccv_parameters_ui('mccv_parameters'),
            width = 2
        ),
        main = ui.navset_tab_card(
                ui.nav('Tables',ui.output_data_frame('tables')),
                ui.nav('Plots',ui.output_ui('plots'))
            )
    )
@module.server
def mccv_results_server(input,output,session,mccv_obj):
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
            mccv_data()['Performance'].groupby(['model','metric'])['value'].describe(percentiles=[0.025,0.975]).reset_index()
        )