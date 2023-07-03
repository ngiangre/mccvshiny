from shiny import App, reactive, render, ui, module
from htmltools import css
import seaborn as sns

@module.ui
def generate_data_ui(label: str = "simulate"):
    return     ui.panel_main(
        {"style": "border: 1px solid #ccc; border-radius: 5px; margin: 5px 0;"},
        ui.div(
            ui.input_selectize('dist','Distribution Type',choices = ['Normal','T','Beta'],multiple=False,width = '200px'),
            ui.output_ui('dist_params'),
            style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
            )
        ),
        ui.output_plot('dist_plot')
    )

@module.server
def generate_data_server(input, output, session):
    
    @output
    @render.ui
    def dist_params():
        return 'Placeholder'
    
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
