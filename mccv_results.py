from shiny import App, reactive, render, ui, module
from htmltools import css

from mccv_parameters import mccv_parameters_ui, mccv_parameters_server

import numpy as np
import pandas as pd
from plotnine import *

import asyncio

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
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Learning in progress", detail="This may take a while...")
            mccv_obj.run_mccv()
            p.set(message="Permutation Learning in progress", detail="This may take a while...")
            mccv_obj.run_permuted_mccv()
        return mccv_obj.mccv_data
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def ml_df():
        return pd.concat([
            (mccv_obj.mccv_data['Model Learning'].
                melt(id_vars = ['bootstrap','model']).
                eval('learning = "real"')
                ),
            (mccv_obj.mccv_permuted_data['Model Learning'].
                melt(id_vars = ['bootstrap','model']).
                eval('learning = "permuted"')
                )
            ])
    
    @output
    @render.plot
    @reactive.event(ml_df)
    def model_performance():
        tmp = ml_df().copy()
        return (ggplot(
                    data=tmp,
                    mapping=aes(x='model',y='value',group='variable'))
                + geom_violin(
                        position=position_dodge(width=0.75),
                        color='lightgrey',
                        size=3)
                + geom_boxplot(
                        data=tmp.query("learning=='real'"),
                        color='black',
                        size=2,
                        alpha=0
                        )
                + geom_point(
                    data=tmp.query("learning=='real'"),
                    mapping=aes(color='variable'),
                    position=position_jitterdodge(jitter_width=0.2),
                    size=3,alpha=0.7)
                + scale_color_brewer(type='qual',palette=1) 
                + guides(color=guide_legend(title='',ncol=1))
                + scale_y_continuous(limits=[0,1]) 
                + theme_bw() 
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x': '','y': 'AUROC'},title='Model Learning')
                )
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def f_imp_df():
        return (mccv_obj.mccv_data['Feature Importance'].
                set_index(['bootstrap','model','feature']).
                join(
                    mccv_obj.mccv_permuted_data['Feature Importance'].
                    rename(columns={'importance' : 'permuted_importance'}).
                    set_index(['bootstrap','model','feature'])
                ).
                reset_index()
                )
    
    @output
    @render.plot
    @reactive.event(f_imp_df)
    def feature_importance():
        pos = position_dodge(width = 0.7)
        tmp = f_imp_df().copy()
        return (ggplot(tmp,
                       aes(x='model',y='importance',color='feature'))
                + geom_violin(
                    mapping=aes(x='model',y='permuted_importance',
                                group='feature'),
                    position=position_dodge(width = .7),
                    color='lightgrey',
                    size=3)
                + geom_boxplot(size=2) 
                + geom_jitter(size=3,
                              position = position_jitterdodge(jitter_width = 0.2))
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
        return (pd.concat([
            mccv_obj.mccv_data['Performance'].eval('learning="real"'),mccv_obj.mccv_permuted_data['Performance'].eval('learning="permuted"')
            ]))
    
    @output
    @render.plot
    @reactive.event(preds_df)
    def model_prediction():
        tmp = preds_df().copy()
        return (ggplot(tmp.query('learning=="real"'),aes(x='model',
                                                         y='value'))
                + geom_violin(data=tmp.query('learning=="permuted"'),color="lightgrey",size=2)
                + geom_boxplot(alpha=0) 
                + geom_point(shape='o',size=3,position=position_jitter(width=0.2))
                + theme_bw()
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x' : '','y' : 'AUROC'},
                    title="Model Prediction",)
                )
    
    @reactive.Calc
    @reactive.event(mccv_data)
    def pt_preds_df():
        return (pd.concat([
                    mccv_obj.mccv_data['Patient Predictions'].
                                groupby(['bootstrap','model','y_true'])['y_proba'].mean().
                                reset_index().
                                eval('learning="real"'),
                    mccv_obj.mccv_permuted_data['Patient Predictions'].
                                groupby(['bootstrap','model','y_true'])['y_proba'].mean().
                                reset_index().
                                eval('learning="permuted"')
                ]))
    
    @output
    @render.plot
    @reactive.event(pt_preds_df)
    def patient_prediction():
        tmp = pt_preds_df().copy()
        tmp['y_true'] = tmp['y_true'].astype('int').astype('object')
        return (ggplot(tmp.query('learning=="real"'),
                        mapping=aes(x='y_true',y='y_proba',color='y_true'))
                + geom_violin(data=tmp.query('learning=="permuted"'),color="lightgrey",size=2)
                + geom_boxplot(alpha=0)
                + geom_point(shape='o',size=3,position=position_jitter(width=0.2))
                + scale_color_brewer(type='qual',palette=3)
                + scale_y_continuous(limits=[0,1])
                + theme_bw()
                + theme(text=element_text(face='bold'),
                        legend_position='bottom')
                + labs(**{'x' : '','y' : 'Patient Probability'},
                    title="Subject Prediction")
                )

    @output
    @render.data_frame
    @reactive.event(mccv_data)
    def summary():
        return render.DataGrid(
            mccv_data()['Performance'].groupby(['model','metric'])['value'].describe(percentiles=[0.025,0.975]).reset_index()
        )