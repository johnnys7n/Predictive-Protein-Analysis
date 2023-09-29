# importing the libraries
import pandas as pd
import numpy as np
from joblib import load, dump

from sklearn.ensemble import RandomForestClassifier

import gradio as gr

with gr.Blocks(theme='abidlabs/dracula_revamped') as app:
    gr.Markdown(
        '''
        <h1 align="center">Welcome to the Age Predictor</h1>
    
        <h2 align="center">Here I will try to predict your age using the contents of your plasma! (...Specifically the Proteins)</h2>

        **NOTE**: This is only a working simulation of applying this methodology for different models and testing multiple combinations of protein values to change the "age" outcome
        
        <p align="center">
            <img src="https://www.sinjohnny.com/static/img/portfolio/age_diagram.png">
        </p>
        '''
    )
    # labeling
    with gr.Row():
        protein_1_input = gr.Number(label="Enter protein_1")
        protein_2_input = gr.Number(label="Enter protein_2")
        protein_3_input = gr.Number(label="Enter protein_3")
        protein_4_input = gr.Number(label="Enter protein_4")
        protein_5_input = gr.Number(label="Enter protein_5")
        protein_6_input = gr.Number(label="Enter protein_6")
        protein_7_input = gr.Number(label="Enter protein_7")
        protein_8_input = gr.Number(label="Enter protein_8")
        protein_9_input = gr.Number(label="Enter protein_9")
        protein_10_input = gr.Number(label="Enter protein_10")
        protein_11_input = gr.Number(label="Enter protein_11")
        protein_12_input = gr.Number(label="Enter protein_12")
        protein_13_input = gr.Number(label="Enter protein_13")
    with gr.Row():
        output = gr.Number(label='The predicted age of the mouse (in months) is....')


    def make_prediction(*args):
        # converting the input into an array
        protein_list = []
        for arg in args:
            protein_list.append(arg)
        
        # the column names for the input test dataset
        col_names = ['protein_1', 'protein_5', 'protein_7', 'protein_8', 'protein_10', 'protein_11', 'protein_12', 'protein_13',
        'protein_14', 'protein_15', 'protein_16','protein_17', 'protein_18']
        # creating this input into a dataframe with appropriate col_names

        df_test = pd.DataFrame(protein_list, index = col_names).T
        with open("rs_rf_reg_model_1.joblib", "rb") as model:
            reg = load(model)
            preds = reg.predict(df_test)[0]
        return preds
    
    submit = gr.Button('Predict!')
    submit.click(
        fn=make_prediction,
        inputs=[
            protein_1_input, 
            protein_2_input, 
            protein_3_input, 
            protein_4_input, 
            protein_5_input, 
            protein_6_input, 
            protein_7_input, 
            protein_8_input,
            protein_9_input,
            protein_10_input,
            protein_11_input,
            protein_12_input,
            protein_13_input
        ],
        outputs=output
    )


if __name__ == "__main__":
    app.launch()
