from shiny import App, reactive, render, ui, module
from htmltools import css

import numpy as np
import seaborn as sns

@module.ui
def generate_data_ui(label: str = "simulate"):
    return  ui.layout_sidebar(
                sidebar = ui.div(
                    ui.input_slider('n','N',
                                    min=50,max=500,step=50,value=50,
                                    ticks=False,width='200px'),
                    ui.input_selectize('dist','Distribution Type',
                                    choices = {'normal' : 'Normal','t' : 'T','beta' : 'Beta'},multiple=False,width = '200px'),
                    ui.input_slider('param1','Parameter 1',min=0,max=1,step=0.1,value=0),
                    ui.input_slider('param2','Parameter 2',min=0,max=1,step=0.1,value=0)
                ),
                main = ui.output_plot('dist_plot')
            )

@module.server
def generate_data_server(input, output, session):
    
    @reactive.Calc
    @reactive.event(input.dist)
    def dist_func():
        rng = np.random.default_rng(0)
        return getattr(rng,input.dist)
    
    @reactive.Effect
    def _():
        if input.dist()=='normal':
            ui.update_slider('param1',label='mu',min=-5,max=5,value=0,step=.1)
            ui.update_slider('param2',label='sigma',min=1,max=5,value=1,step=1)
        if input.dist()=='t':
            ui.update_slider('param1',label='mu',min=-5,max=5,value=0,step=.1)
            ui.update_slider('param2',label='df',min=1,max=5,value=1,step=1)
        if input.dist()=='beta':
            ui.update_slider('param1',label='a',min=0,max=5,value=1,step=.1)
            ui.update_slider('param2',label='b',min=0,max=5,value=1,step=.1)
    
    @output
    @render.plot
    def dist_plot():
        sns.set_theme(style="ticks", palette="pastel")

        # Load the example tips dataset
        tips = sns.load_dataset("tips")

        # Draw a nested boxplot to show bills by day and time
        sns.boxplot(x="day", y="total_bill",
                    hue="smoker", palette=["m", "g"],
                    data=tips)
        sns.despine(offset=10, trim=True)
