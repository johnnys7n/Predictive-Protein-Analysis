import pandas as pd
import numpy as np
import gradio as gr
import os
from pathlib import Path
from io import StringIO
import sys

# new name input
new_filename = gr.Textbox('Please write the name of the newly joined file')

# file_1 input
file_1 = gr.File(
    label="please insert the data file",
    file_types=[".csv", ".xlsx"],
    file_count="single", 
    type = 'file'
)
file_1_ID = gr.Textbox('please indicate the ID column for file 1')

# file_2 input
file_2 = gr.File(
    label="please insert the id file", file_types=[".csv", ".xlsx"], file_count="single", type = 'file'
)

file_2_ID = gr.Textbox('please indicate the ID column for file 2')

# creating a function using the pandas class to join the dataframe inputs 
def join_csv(joined_filename, file_1_col_name, file_data, file_2_col_name, file_ID):
    '''
    # Parameters:
    1. joined_filename: new name for the join file, which will be saved on the working dir (str) 
    2. file_1_col_name: the ID / index of file 1 (str)
    3. file_data: intial file (.csv or .xlsx)
    4. file_2_col_name: the ID / index of file 2 (str)
    5. file_ID: file to join and populate file_data
    '''
    with open(str(file_data.name),'rb') as file_data_, open(str(file_ID.name),'rb') as file_ID_:
        file_path_1 = Path(file_data.name)
        file_path_2 = Path(file_ID.name)
        if file_path_1.suffix =='.csv':
            df1 = pd.read_csv(file_data_.name)
        else:
            df1 = pd.read_excel(file_data_.name)
        if file_path_2.suffix =='.csv':
            df2 = pd.read_csv(file_ID_.name)
        else:
            df2 = pd.read_excel(file_ID_.name)
    df3 = df1.set_index(file_1_col_name).join(df2.set_index(file_2_col_name))
    return df3.to_csv(str(joined_filename) + '.csv')

output = gr.File(
    label="Output File",
    file_types=[".csv", ".xlsx"],
    file_count="single", 
    type = 'file'
)

demo = gr.Interface(fn=join_csv, inputs=[new_filename, file_1_ID, file_1, file_2_ID, file_2], outputs=output,
                    title = 'Joining CSV files by ID',
                    theme='finlaymacklon/smooth_slate')

if __name__ == "__main__":
    demo.launch(share=False)