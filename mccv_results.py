from shiny import App, reactive, render, ui, module
from htmltools import css

from mccv_parameters import mccv_parameters_ui, mccv_parameters_server

from plotnine import *

@module.ui
def mccv_results_ui(label: str = 'mccv_parameters'):
    return ui.layout_sidebar(
        sidebar = ui.panel_sidebar(
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            mccv_parameters_ui('mccv_parameters'),
            width = 2
        ),
        main = ui.navset_tab_card(
                ui.nav('Model Performance',
                       ui.output_plot('model_performance')),
                ui.nav('Feature Importance',
                       ui.output_plot('feature_importance')),
                ui.nav('Tables',
                       ui.output_data_frame('tables')
                       )
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
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def ml_df():
        return (mccv_obj.mccv_data['Model Learning'].
                melt(id_vars = ['bootstrap','model'])
                )
    
    @output
    @render.plot
    @reactive.event(ml_df)
    def model_performance():
        return (ggplot(ml_df(),aes(x='model',y='value',color='variable'))
                + geom_boxplot(alpha=0)
                + geom_point(aes(group='variable'),size=3,position=position_jitterdodge(dodge_width = 0.7,jitter_width = 0.1))
                + scale_color_brewer(type='qual',palette=2) 
                + scale_y_continuous(limits=[0,1]) 
                + theme_bw() 
                + theme(text=element_text(face='bold'))
                + labs(**{'x': '','y': 'Metric Value'})
                )
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def f_imp_df():
        return (mccv_obj.mccv_data['Feature Importance'])
    
    @output
    @render.plot
    @reactive.event(f_imp_df)
    def feature_importance():
        return (ggplot(f_imp_df(),aes(x='model',y='importance',
                                      color='feature'))
                + geom_boxplot(alpha=0) 
                + geom_point(size=3,
                             position=position_jitter(width=0.2))
                + scale_color_brewer(type='qual',palette=2)
                + theme_bw()
                + theme(text=element_text(face='bold'))
                + labs(**{'x': '','y': 'Feature Importance'})
                )
    @output
    @render.data_frame
    @reactive.event(mccv_data)
    def tables():
        return render.DataGrid(
            mccv_data()['Performance'].groupby(['model','metric'])['value'].describe(percentiles=[0.025,0.975]).reset_index()
        )