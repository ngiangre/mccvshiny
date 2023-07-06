from shiny import App, reactive, render, ui, module
from htmltools import css

import numpy as np
import pandas as pd
import seaborn as sns

@module.ui
def generate_data_ui(label: str = "simulate"):
    return  ui.layout_sidebar(
                sidebar = ui.div(
                    ui.input_slider('n','N',
                                    min=50,max=500,step=50,value=50,
                                    ticks=False,width='200px'),
                    ui.input_selectize('dist','Distribution Type',
                                    choices = {'normal' : 'Normal','beta' : 'Beta'},multiple=False,width = '200px'),
                    ui.input_slider('param1','Parameter 1',min=0,max=1,step=0.1,value=0),
                    ui.input_slider('param2','Parameter 2',min=0,max=1,step=0.1,value=0),
                    ui.input_slider('prop_class1',label='Proportion of Class 1',min=0,max=1,value=0.5,step=0.1)
                ),
                main = ui.navset_tab_card(
                    ui.nav('Table',
                           ui.output_data_frame('dist_table')),
                    ui.nav('Plot',
                           ui.output_plot('dist_plot'))
                    )
            )

@module.server
def generate_data_server(input, output, session):
    
    rng = np.random.default_rng(0)
    
    @reactive.Calc
    @reactive.event(input.dist)
    def dist_func():
        return getattr(rng,input.dist())
    
    @reactive.Effect
    def _():
        if input.dist()=='normal':
            ui.update_slider('param1',label='mu',min=-5,max=5,value=0,step=.1)
            ui.update_slider('param2',label='sigma',min=1,max=5,value=1,step=1)
        if input.dist()=='t':
            ui.update_slider('param1',label='mu',min=-5,max=5,value=0,step=.1)
            ui.update_slider('param2',label='df',min=1,max=5,value=1,step=1)
        if input.dist()=='beta':
            ui.update_slider('param1',label='a',min=1,max=5,value=1,step=.1)
            ui.update_slider('param2',label='b',min=1,max=5,value=1,step=.1)
    
    @reactive.Calc
    def data_generator():
        arr = dist_func()(input.param1(),
                            input.param2(),
                            size=input.n())
        statuses = np.ones(input.n())
        arr_sorted = np.sort(arr)
        n_class0 = int(input.n()*(1-input.prop_class1()))
        statuses[np.arange(1,n_class0)] = 0
        return pd.DataFrame({'result' : list(arr_sorted),'status' : list(statuses)})
        
    @output
    @render.data_frame
    def dist_table():
        return render.DataGrid(
            data_generator(),
            width="100%",
            height="100%")
    
    @output
    @render.plot
    def dist_plot():
        return sns.histplot(data_generator(),x='result',hue='status')
