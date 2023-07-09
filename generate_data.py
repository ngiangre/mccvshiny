from shiny import App, reactive, render, ui, module
from htmltools import css

import numpy as np
import pandas as pd
import seaborn as sns

def generate_arrays(class1_size, effect_size, input_array):
    '''
    We calculate the lengths of the two classes based on the class1_size input, ensuring that their sum equals the length of the input_array.
    We calculate the mean difference between the two output arrays by multiplying the effect_size input with the standard deviation of the input_array.
    We create the class1_array by taking the first class1_length elements of the input_array and adding the mean difference.
    We create the class0_array by taking the remaining elements of the input_array and subtracting the mean difference.
    Finally, we return the two output arrays: class1_array and class0_array.
    '''
    class1_length = int(class1_size * len(input_array))
    class0_length = len(input_array) - class1_length
    
    mean_diff = effect_size * np.std(input_array)
    
    class1_array = input_array[:class1_length] + mean_diff
    class0_array = input_array[class1_length:] - mean_diff
    
    return class1_array, class0_array

@module.ui
def generate_data_ui(label: str = "simulate"):
    return  ui.layout_sidebar(
                sidebar = ui.div(
                    ui.input_slider('n','N',
                                    min=50,max=500,step=50,value=100,
                                    ticks=False,width='200px'),
                    ui.input_selectize('dist','Distribution Type',
                                    choices = {'normal' : 'Normal','beta' : 'Beta'},multiple=False,width = '200px'),
                    ui.input_slider('param1','Parameter 1',min=0,max=1,step=0.1,value=0,ticks=False,width='200px'),
                    ui.input_slider('param2','Parameter 2',min=0,max=1,step=0.1,value=0,ticks=False,width='200px'),
                    ui.input_slider('prop_class1',label='Proportion of Class 1',min=0.2,max=0.8,value=0.5,step=0.1,ticks=False,width='200px'),
                    ui.input_slider('std_diff',label='Class 1 Mean Difference',min=0,max=1,value=0,step=0.1,ticks=False,width='200px')
                ),
                main = ui.navset_tab_card(
                    ui.nav('Plot',
                           ui.output_plot('dist_plot')),
                    ui.nav('Table',
                           ui.output_data_frame('dist_table'))
                    )
            )

@module.server
def generate_data_server(input, output, session,mccv_obj):
    
    seed = 0
    rng = np.random.default_rng(seed)
    mccv_obj.seed = seed
    
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
        array1, array0 = generate_arrays(input.prop_class1(),input.std_diff(), arr)
        return pd.DataFrame({'result' : np.concatenate([array1,array0]),
                             'class' : np.concatenate([np.ones(len(array1)),np.zeros(len(array0))])})
        
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
        mccv_obj.set_X(data_generator().loc[:,['result']])
        mccv_obj.set_Y(data_generator().loc[:,['class']])
        return sns.histplot(data_generator(),x='result',hue='class')
