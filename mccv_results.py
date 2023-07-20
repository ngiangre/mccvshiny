from shiny import App, reactive, render, ui, module
from htmltools import css

from mccv_parameters import mccv_parameters_ui, mccv_parameters_server

import numpy as np
from plotnine import *

@module.ui
def mccv_results_ui(label: str = 'mccv_parameters'):
    return ui.layout_sidebar(
        sidebar = ui.panel_sidebar(
            ui.input_action_button('run_model','Run MCCV',class_="btn-primary"),
            mccv_parameters_ui('mccv_parameters'),
            width = 2
        ),
        main = ui.column(12,
                       ui.row(
                           ui.column(3,ui.output_plot('model_performance')),
                           ui.column(3,ui.output_plot('feature_importance')),
                           ui.column(3,ui.output_plot('model_prediction')),
                           ui.column(3,ui.output_plot('patient_prediction'))
                           ),
                       ui.tags.hr(),
                       ui.output_data_frame('summary')
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
                + scale_color_brewer(type='qual',palette=1) 
                + guides(color=guide_legend(title='',ncol=1))
                + scale_y_continuous(limits=[0,1]) 
                + theme_bw() 
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x': '','y': 'AUROC'},
                       title='Model Learning')
                )
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def f_imp_df():
        return (mccv_obj.mccv_data['Feature Importance'])
    
    @output
    @render.plot
    @reactive.event(f_imp_df)
    def feature_importance():
        pos = position_dodge(width = 0.7)
        return (ggplot(f_imp_df(),aes(x='model',y='importance',
                                      color='feature'))
                + geom_boxplot(alpha=0,
                             position=pos) 
                + geom_jitter(size=3,
                              position = position_jitterdodge(dodge_width = 0.7,jitter_width = 0.1))
                + scale_color_brewer(type='qual',palette=2)
                + theme_bw()
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x': '','y': 'Feature Importance'},
                       title='Feature Importance')
                )
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def preds_df():
        return (mccv_obj.mccv_data['Performance'])
    
    @output
    @render.plot
    @reactive.event(preds_df)
    def model_prediction():
        return (ggplot(preds_df(),aes(x='model',y='value'))
                + geom_boxplot(alpha=0) 
                + geom_point(shape='o',size=3,position=position_jitter(width=0.2))
                + theme_bw()
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x' : '','y' : 'AUROC'},
                    title="Model prediction",)
                )
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def pt_preds_df():
        return (mccv_obj.mccv_data['Patient Predictions'].
                groupby(['bootstrap','model','y_true'])['y_proba'].mean().
                reset_index())
    
    @output
    @render.plot
    @reactive.event(pt_preds_df)
    def patient_prediction():
        tmp = pt_preds_df().copy()
        tmp['y_true'] = tmp['y_true'].astype('int').astype('object')
        return (ggplot(tmp,
                       aes(x='y_true',y='y_proba',color='y_true'))
                + geom_boxplot(alpha=0)
                + geom_point(shape='o',size=3,position=position_jitter(width=0.2))
                + scale_color_brewer(type='qual',palette=3)
                + scale_y_continuous(limits=[0,1])
                + theme_bw()
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x' : '','y' : 'Patient Probability'},
                    title="Subject predictions")
                )

    @output
    @render.data_frame
    @reactive.event(mccv_data)
    def summary():
        return render.DataGrid(
            mccv_data()['Performance'].groupby(['model','metric'])['value'].describe(percentiles=[0.025,0.975]).reset_index()
        )