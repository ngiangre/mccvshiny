from shiny import App, reactive, render, ui, module
from htmltools import css

import numpy as np
import pandas as pd
from plotnine import *

import numpy as np

def generate_arrays(class1_size, effect_size, input_array):
    
    # Calculate the sizes of the two output arrays
    class1_length = int(class1_size * len(input_array))
    class0_length = len(input_array) - class1_length

    # Calculate the difference in means required to achieve the desired effect size
    mean_diff = effect_size * np.std(input_array)

    # Randomly shuffle the input_array to avoid any bias
    np.random.shuffle(input_array)

    # Split the shuffled array into two arrays based on the class1_size
    class1_array = input_array[:class1_length]
    class0_array = input_array[class1_length:]

    # Calculate the mean of the two arrays
    mean_class1 = np.mean(class1_array)
    mean_class0 = np.mean(class0_array)

    # Shift the means to achieve the desired mean difference

    class1_array += mean_diff / 2
    class0_array -= mean_diff / 2

    return class1_array, class0_array

def calculate_bin_width(data_array):
    #https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.geom_density.html#plotnine.geoms.geom_density
    #and chatgpt
    
    # Sort the data in ascending order
    sorted_data = np.sort(data_array)
    
    # Calculate the interquartile range (IQR)
    q1 = np.percentile(sorted_data, 25)
    q3 = np.percentile(sorted_data, 75)
    iqr = q3 - q1
    
    # Calculate the number of data points
    n = len(sorted_data)
    
    # Calculate the bin width using the Freedman-Diaconis rule 
    bin_width = (2.0 * iqr * n**(-1/3))
    
    return bin_width

@module.ui
def generate_data_ui(label: str = "simulate"):
    return  ui.layout_sidebar(
                sidebar = ui.panel_sidebar(
                    ui.input_slider('n','N',
                                    min=100,max=1000,step=50,value=500,
                                    ticks=False),
                    ui.input_selectize('dist','Distribution Type',
                                    choices = {
                                        'normal' : 'Normal',
                                        'lognormal' : 'Log Normal',
                                        'chisquare' : 'Chi Square',
                                        'beta' : 'Beta',
                                        'standard_t' : "Student's T",
                                        'pareto' : 'Pareto'},multiple=False),
                    ui.output_ui('dist_params'),
                    ui.input_slider('prop_class1',label='Class 1 Proportion',min=0.2,max=0.8,value=0.5,step=0.1,ticks=False),
                    ui.input_slider('std_diff',label="Average Class Offset",min=-2,max=2,value=0,step=0.1,ticks=False),
                    width = 2
                ),
                main = ui.navset_tab_card(
                    ui.nav('Plot',
                           ui.row(
                               ui.column(6,
                                   ui.output_plot('dist_histplot')
                                   ),
                               ui.column(6,
                                   ui.output_plot('dist_boxplot')
                                   )
                               )
                           ),
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
    
    @output
    @render.ui
    @reactive.event(input.dist,input.n)
    def dist_params():
        if input.dist()=='normal':
            return ui.TagList(
                ui.input_slider('param1','Parameter 1',min=-5,max=5,step=0,value=1,ticks=False),
                ui.input_slider('param2','Parameter 2',min=1,max=5,step=1,value=1,ticks=False)
            )
        if input.dist()=='beta':
            return ui.TagList(
                ui.input_slider('param1','Parameter 1',min=1,max=5,value=1,step=1,ticks=False),
                ui.input_slider('param2','Parameter 2',min=1,max=5,value=1,step=1,ticks=False)
            )
        if input.dist()=='lognormal':
            return ui.TagList(
                ui.input_slider('param1','Parameter 1',min=0,max=10,step=1,value=0,ticks=False),
                ui.input_slider('param2','Parameter 2',min=1,max=10,step=1,value=1,ticks=False)
            )
        if input.dist()=='chisquare':
            return ui.TagList(
                ui.input_slider('param1','Parameter 1',min=1,max=10,step=1,value=1,ticks=False)
            )
        if input.dist()=='pareto':
            return ui.TagList(
                ui.input_slider('param1','Parameter 1',min=1,max=10,step=1,value=2,ticks=False)
            )
        if input.dist()=='standard_t':
            return ui.TagList(
                ui.input_slider('param1','Parameter 1',min=2,max=10,step=1,value=10,ticks=False)
            )
    @reactive.Effect
    @reactive.event(input.dist,input.n)
    def _():
        if input.dist()=='normal':
            ui.update_slider('param1',label='loc',min=-5,max=5,value=0,step=1)
            ui.update_slider('param2',label='scale',min=1,max=5,value=1,step=1)
        if input.dist()=='lognormal':
            ui.update_slider('param1',label='mean',min=0,max=10,value=0,step=1)
            ui.update_slider('param2',label='sigma',min=1,max=10,value=1,step=1)
        if input.dist()=='chisquare':
            ui.update_slider('param1',label='df',min=1,max=10,value=1,step=1)
        if input.dist()=='pareto':
            ui.update_slider('param1',label='a',min=1,max=10,value=2,step=1)
        if input.dist()=='standard_t':
            ui.update_slider('param1',label='df',min=2,max=10,value=10,step=1)
        if input.dist()=='beta':
            ui.update_slider('param1',label='a',min=1,max=5,value=1,step=1)
            ui.update_slider('param2',label='b',min=1,max=5,value=1,step=1)
    
    @reactive.Calc
    @reactive.event(input.dist,input.param1,input.param2,input.n)
    def dist_param_dict():
        if input.dist()=='normal':
            return {'loc' : input.param1(),
                    'scale' : input.param2(),
                    'size' : input.n()}
        if input.dist()=='lognormal':
            return {'mean' : input.param1(),
                    'sigma' : input.param2(),
                    'size' : input.n()}
        if input.dist()=='negative_binomial':
            return {'n' : np.max([input.param1(),2]),
                    'p' : input.param2(),
                    'size' : input.n()}
        if input.dist()=='chisquare':
            return {'df' : np.max([input.param1(),1]),
                    'size' : input.n()}
        if input.dist()=='pareto':
            return {'a' : np.max([input.param1(),1]),
                    'size' : input.n()}
        if input.dist()=='standard_t':
            return {'df' : np.max([input.param1(),2]),
                    'size' : input.n()}
        if input.dist()=='beta':
            return {'a' : np.max([input.param1(),1]),
                    'b' : np.max([input.param2(),1]),
                    'size' : input.n()}
        
    @reactive.Calc
    @reactive.event(input.dist,dist_param_dict,input.prop_class1,input.std_diff)
    def data_generator():
        tmp = dist_param_dict().copy()
        arr = dist_func()(**tmp)
        array1, array0 = generate_arrays(input.prop_class1(),input.std_diff(), arr)
        return pd.DataFrame({'result' : np.concatenate([array1,array0]),
                             'class' : np.concatenate([np.ones(len(array1)),np.zeros(len(array0))])})
        
    @output
    @render.data_frame
    def dist_table():
        return data_generator()
    
    @reactive.Effect
    @reactive.event(data_generator)
    def _():
        mccv_obj.set_X(data_generator().loc[:,['result']])
        mccv_obj.set_Y(data_generator().loc[:,['class']])
        
    @output
    @render.plot
    @reactive.event(data_generator)
    def dist_histplot():
        tmp = data_generator().copy()
        tmp['class'] = tmp['class'].astype('int64').astype('object')
        binwidth_ = calculate_bin_width(tmp.result.values)
        if binwidth_<=0:
            binwidth_ = 0.5
        return (ggplot(tmp,aes(x='result',fill='class'))
                + geom_density(data=tmp,
                               mapping=aes(x='result',
                                           y=after_stat('count*binwidth_')),
                                 alpha=0.5,inherit_aes=False,
                                 size=2,
                                 color='darkgray',fill='darkgray')
                + geom_histogram(mapping=aes(y=after_stat('count')),
                                 binwidth=binwidth_,position='identity',alpha=0.5,color='black')
                + labs(x='Result',y='Number in Class',caption='Result distribution shape in gray')
                + scale_fill_manual(values=['cornflowerblue','indianred'])
                + theme_bw()
                + theme(text=element_text(family='Times',size=16)))
    
    @output
    @render.plot
    def dist_boxplot():
        tmp = data_generator().copy()
        tmp['class'] = tmp['class'].astype('int64').astype('object')
        return (ggplot(tmp,aes(x='class',y='result',color='class'))
                + geom_violin(size=2)
                + geom_boxplot(color='black',size=2)
                + geom_jitter(size=3,width=0.2) 
                + labs(y='Result',x='Class')
                + scale_color_manual(values=['cornflowerblue','indianred'])
                + theme_bw()
                + theme(text=element_text(family='Times',size=16)))
    
