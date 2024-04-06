import pandas as pd

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

import plotly.express as px
from PIL import Image

def run():
    st.set_page_config(
        page_title="Survey Results",
        page_icon="👋",
    )

    st.header('Survy Results 2021')
    st.subheader('Was the tutorial helpful?')

    ### --- LOAD DATAFRAME
    excel_file = "Survey_Results.xlsx"
    sheet_name = 'DATA'

    df = pd.read_excel(excel_file,
                       engine="openpyxl",
                       sheet_name=sheet_name,
                       usecols='B:D',
                       header=3)
    
    df_participants = pd.read_excel(excel_file,
                                    engine="openpyxl",
                                    sheet_name=sheet_name,
                                    usecols='F:G',
                                    header=3)
    
    # drop the NA values in the partipicants data
    df_participants.dropna(inplace=True)

    # --- STREAMLIT SECTION
    department = df['Department'].unique().tolist()
    ages = df['Age'].unique().tolist()

    age_selection = st.slider('Age:',
                              min_value= min(ages),
                              max_value= max(ages),
                              value=(min(ages),max(ages)))
    
    department_selection = st.multiselect('Department:',
                                          department,
                                          default=department)
    
    # --- FILTER DATAFRAME BASED ON SELECTION
    mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Results: {number_of_result}*')

    # --- GROUP DATAFRAME AFTER SELECTION
    df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
    df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
    df_grouped = df_grouped.reset_index()

    # --- PLOT BAR CHART
    bar_chart = px.bar(df_grouped,
                       x='Rating',
                       y='Votes',
                       text='Votes',
                       color_discrete_sequence = ['#F63366']*len(df_grouped),
                       template= 'plotly_white')
    st.plotly_chart(bar_chart)

    # --- DISPLAY IMAGE & DATAFRAME
    # Refactor the page to show the image and dataframe in columns next to each other
    col1, col2 = st.columns(2)
    image = Image.open('images/survey.jpg')
    col1.image(image,
             caption='Designed by slidesgo / Freepik',
             use_column_width=True)
             #width=200)
    col2.dataframe(df[mask])
    


    pie_chart = px.pie(df_participants,
                       title='Total No. of Participants',
                       values='Participants',
                       names='Departments')

    st.plotly_chart(pie_chart)

   

if __name__ == "__main__":
    run()
