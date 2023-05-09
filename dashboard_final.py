import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.express as px 
import time 
import streamlit.components.v1 as components
from PIL import Image 

st.set_page_config(
    page_title="LaLL App",
    page_icon="🌱",
    layout="wide"
)


example_image1 = Image.open("./PlantImage/2023-04-14/7-15-57.jpg")
#st.image(example_image1,caption="1号架子",use_column_width=True)
example_image2 = Image.open("./PlantImage/2023-04-14/2-15-57.jpg")
#st.image(example_image2,caption="2号架子",use_column_width=True)
example_image3 = Image.open("./PlantImage/2023-04-14/4-15-57.jpg")
#st.image(example_image3,caption="3号架子",use_column_width=True)

sample_ims = {
    'im1':example_image1,
    'im2':example_image2,
    'im3':example_image3
}

import os 

csv_path = "./arranged_data4"
files = os.listdir(csv_path)
num_files = len(files)
dataframes4 = {}

for i in range(10,num_files): #有效数据
    dataframes4['df'+str(i)] = pd.read_csv('arranged_data4/sub_df'+str(i)+'.csv')

hetero_collection = []
for i in range(1,10):
    hetero_collection.append(pd.read_csv('./hetero_data/hetero_'+str(i)+'.csv'))

df_dict = {}
light_period = [16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8]
dark_period = [9,10,11,12,13,14,15]

light_co2_consum = []
dark_co2_consum = []

combine_df = dataframes4['df10']

for i in range(10,num_files):
    combine_df=pd.concat((combine_df,dataframes4['df'+str(i)]))

combine_df['time'] = pd.to_datetime(combine_df['time'])
combine_df = combine_df.set_index('time')
combine_df['time'] = combine_df.index
combine_df['顺序'] = [i for i in range(1,len(combine_df)+1)]

from datetime import datetime,time

_,main_col,_ = st.columns((1,2,1))
times = combine_df['time']
with main_col:
    st.title("生生不息数据平台")
    stuff = """
    values = st.slider(
'选择时间段',
    min_value=datetime(times[0].year,times[0].month,times[0].day), 
    max_value=datetime(times[-1].year,times[-1].month,times[-1].day), 
    value=(datetime(times[30].year,times[30].month,times[30].day), 
            datetime(times[200].year,times[100].month,times[100].day))
    ,#step=datetime(year=2023,month=1,day=1,hour=1,minute=1),
    format="MM/DD")
    """
    
def enviro_module():
    to_fix = """
    st.markdown("## 种植进度")
    f21, f22 = st.columns(2)
    f21.metric(label = "🌡今日气温",
                value = str(round(combine_df['户外温度'][-1],2)),
                delta = str(round(combine_df['户外温度'][-1]-combine_df['户外温度'][-2],2)),
                ) 
    f21.metric(label = "当前室温",
                value = str(round(combine_df['平均温度'][-1],2)),
                delta = str(round(combine_df['平均温度'][-1]-combine_df['平均温度'][-2],2)))

    f22.metric(label = "💧室外湿度(%)",
                value = str(round(combine_df['户外湿度'][-1],2)), 
                delta = str(round(combine_df['户外湿度'][-1]-combine_df['户外湿度'][-2],2)))
    f22.metric(label = "相对湿度(%)",
                value = str(round(combine_df['平均湿度'][-1],2)),
                delta = str(round(combine_df['平均湿度'][-1]-combine_df['平均湿度'][-2],2)))

    """
    
    st.markdown("## 历史环境数据")
    start_date = values[0]
    end_date = values[1]

    start_time_diff = combine_df['time'] - pd.to_datetime(start_date)
    start_datetime = start_time_diff.abs().idxmin()

    end_time_diff = combine_df['time'] - pd.to_datetime(end_date)
    end_datetime = end_time_diff.abs().idxmin()

    combine_df_s = combine_df[(combine_df.index >= start_datetime) & (combine_df.index <= end_datetime)]

    f1,f2= st.columns((2,2),gap="medium")
    with f1:
        
        fig = px.line(combine_df_s,x='time',y=['平均温度','1号室内温度','2号室内温度','户外温度'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="温度",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.line(combine_df_s,x='time',y=['1号室内CO2浓度','2号室内CO2浓度'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="CO2浓度",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        #st.line_chart(combine_df,x='顺序',y=['平均温度','1号室内温度','2号室内温度','户外温度'])
        st.markdown("""  ---  """)
        fig = px.line(combine_df_s,x='time',y=['营养液EC'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="营养液EC",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.line(combine_df_s,x='time',y=['1号蓝比','2号蓝比','3号蓝比','1号绿比','2号绿比','3号绿比','1号红比','2号红比','3号红比'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="光谱",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.line(combine_df_s,x='time',y=['1号色温','2号色温','3号色温'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="色温",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)
        #st.area_chart(combine_df,x='顺序',y=['营养液EC'],height=300,use_container_width=True)
    with f2:
        fig = px.line(combine_df_s,x='time',y=['平均湿度','1号室内湿度','2号室内湿度'],height=300,template='plotly_dark')
        fig.update_layout(title="湿度",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        st.plotly_chart(fig,use_container_width=True)

        fig = px.line(combine_df_s,x='time',y=['营养液液温'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="营养液液温",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("""  ---  """)
        fig = px.line(combine_df_s,x='time',y=['营养液PH'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="营养液PH",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.line(combine_df_s,x='time',y=['1号PPFD','2号PPFD','3号PPFD'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="PPFD",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.line(combine_df_s,x='time',y=['1号PAR','2号PAR','3号PAR'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="PAR",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)

    
    st.markdown("## 数据总览")
    try:
        del combine_df['Unnamed: 0']
        del combine_df['Unnamed: 0.1']
    except:
        pass
    st.dataframe(combine_df)

#import sys 
#sys.path.append('./')
from data_display import select_and_show_hetero_data



with st.sidebar:
  module = st.radio('工程模块',['环境参数','异构数据'])
  values = st.slider(
'选择时间段',
    min_value=datetime(times[0].year,times[0].month,times[0].day), 
    max_value=datetime(times[-1].year,times[-1].month,times[-1].day), 
    value=(datetime(times[30].year,times[30].month,times[30].day), 
            datetime(times[200].year,times[100].month,times[100].day))
    ,#step=datetime(year=2023,month=1,day=1,hour=1,minute=1),
    format="MM/DD")
    
  if st.buttong('Clear cache'):
    st.cache_data.clear()

if module == '环境参数':
    enviro_module()
elif module == '异构数据':
    select_and_show_hetero_data()

  