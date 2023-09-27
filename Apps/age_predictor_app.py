# importing the libraries
import pandas as pd
import numpy as np
from joblib import load, dump

from sklearn.ensemble import RandomForestClassifier

import gradio as gr

# labeling
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

output = gr.Number(label='The predicted age of the mouse (in months) is....')


def make_prediction(*args):
    # converting the input into an array
    protein_list = []
    for arg in args:
        protein_list.append(arg)
    
    # the column names for the input test dataset
    col_names = ['protein_1', 'protein_2', 'protein_3', 'protein_4', 'protein_5', 'protein_6', 'protein_7', 'protein_8',
       'protein_9', 'protein_10', 'protein_11', 'protein_12']
    # creating this input into a dataframe with appropriate col_names

    df_test = pd.DataFrame(protein_list, index = col_names).T
    with open("rs_rf_reg_model_1.joblib", "rb") as model:
        reg = load(model)
        preds = reg.predict(df_test)[0]
    return preds

# creating the Gradio interface
app = gr.Interface(
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
        protein_12_input
    ],
    outputs=output, title = 'Mouse Age Predictor (in months) Using Plasma Protein Output', theme='finlaymacklon/smooth_slate'
)
if __name__ == "__main__":
    app.launch(share=False)
