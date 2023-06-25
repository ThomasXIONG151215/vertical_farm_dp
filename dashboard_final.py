import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.express as px 
import time 
import streamlit.components.v1 as components
from PIL import Image 

st.set_page_config(
    page_title="SSBX",
    page_icon="🌱",
    layout="wide"
)

import os 

csv_path = "./arranged_data4"
files = os.listdir(csv_path)
num_files = len(files)-1
dataframes4 = {}

for i in range(10,num_files): #有效数据
    dataframes4['df'+str(i)] = pd.read_csv('./arranged_data4/sub_df'+str(i)+'.csv')

hetero_collection = []
for i in range(1,10):
    hetero_collection.append(pd.read_csv('./hetero_data/hetero_'+str(i)+'.csv'))

df_dict = {}
light_period = [16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8]
dark_period = [9,10,11,12,13,14,15]

light_co2_consum = []
dark_co2_consum = []

#combine_df = dataframes4['df10']

#for i in range(10,num_files):
#    combine_df=pd.concat((combine_df,dataframes4['df'+str(i)]))
combine_df = pd.read_csv('./arranged_data4/sub_df0.csv')

combine_df['time'] = pd.to_datetime(combine_df['time'])
combine_df = combine_df.set_index('time')
combine_df['time'] = combine_df.index
combine_df['顺序'] = [i for i in range(1,len(combine_df)+1)]

from datetime import datetime,time

_,main_col,_ = st.columns((1,0.5,1))
times = combine_df['time']
with main_col:
    st.title("生生不息平台",anchor="center")

def control_pannel():
    st.markdown("## 控制面板")

    st.markdown("### 灯光控制")
    l1, l2 = st.columns(2)
    with l1:
        light_start = st.slider("开启时间",min_value=0,max_value=24,value=18)
        #blue = st.number_input("蓝光",min_value=0,max_value=100,value=20)
        #red = st.number_input("红光",min_value=0,max_value=100,value=40)
        #green = st.number_input("绿光",min_value=0,max_value=100,value=10)
        #large_red = st.number_input("远红光",min_value=0,max_value=100,value=10)
    with l2:
        #st.metric(label = "光照强度",value=str(round((blue+red+green+large_red)/4,1))+" %")
        light_end = st.slider("关闭时间",min_value=0,max_value=24,value=10)
    exec_light = st.button("灯光执行")
    if exec_light:
        light_lenght = 24 - light_start + light_end
        dark_lenght = 24 - light_lenght
        st.session_state.light = st.warning("执行成功，从现在起光期时长为"+str(light_lenght)+"小时, 暗期时长为"+str(dark_lenght)+"小时")

    st.markdown("### 温度控制")
    a1, a2 = st.columns(2)
    with a1:
        ac_onoff = st.checkbox("空调开关")
        T_set = st.number_input("设定温度",min_value=18,max_value=30,value=24)
        #fresh_air_onoff = st.checkbox("新风开关")
        mode = st.selectbox("模式",["制冷","制热","送风","除湿"])
        mode_effect = {
            "制冷": -1,
            "制热": 1,
            "送风": -0.1,
            "除湿": -0.5
        }[mode]
        intensity = st.number_input("风速档位",min_value=0,max_value=7,value=4)
        duration = st.number_input("持续时间(min)",min_value=0,max_value=60,value=2)
        #fresh_air_rate = st.number_input("新风开度",min_value=0,max_value=100,value=20)        
        T_now = 24.7
        T_predict = T_now + ac_onoff*mode_effect*intensity*duration/60
        
        RH_now = 67
        RH_predict = RH_now + ac_onoff*mode_effect*intensity*duration/60 * 3.2

    with a2:
        d1, d2 = st.columns(2)
        
        with d1:
            st.metric(label = "当前温度",value=str(round(T_now,1))+" ℃")
            st.metric(label = "预测温度",value=str(round(T_predict,1))+" ℃",delta=str(round(T_predict-T_now,1))+" ℃")
        
        with d2:
            st.metric(label = "当前湿度",value=str(round(RH_now,1))+" %")
            st.metric(label = "预测湿度",value=str(round(RH_predict,1))+" %",delta=str(round(RH_predict-RH_now,1))+" %")
        T_set_light = st.slider("光期设定温度",min_value=18,max_value=26,value=T_set)
        T_set_night = st.slider("暗期设定温度",min_value=17,max_value=26,value=22)

        ac_exec = st.button("空调执行")
    if ac_exec:
        st.success("执行成功，预计"+str(duration)+"分钟后温度达到"+str(T_predict)+"度与目标值"+str(T_set)+"度相差"+"%s ℃" % round(abs(T_predict-T_set),1)+"同时相对湿度温度维持在60-90%区间")

    st.markdown("### CO2控制")

    c1, c2 = st.columns(2)
    with c1:
        co2_set = st.number_input("CO2设定",min_value=0,max_value=1000,value=900)
        co2_duration = st.number_input("阀门开启时间(s)",min_value=0,max_value=120,value=30)
        step = st.number_input("规划次数",min_value=0,max_value=60,value=10)
        ppm_now = 700
        ppm_predict = ppm_now + step*co2_duration/60*32.4
    with c2:
        st.metric(label = "当前CO2浓度",value=str(ppm_now)+" ppm")
        st.metric(label = "预测CO2浓度",value=str(round(ppm_predict,1))+" ppm",delta=str(round(ppm_predict-ppm_now,1))+" ppm")
        co2_exec = st.button("CO2执行")
    if co2_exec:
        st.info("执行成功，预计二氧化碳浓度调节准确率将达"+"%s %%" % round(100-abs(ppm_predict-co2_set)/co2_set*100,1))

    #change_backend = st.checkbox("修改后台算法")    
    #if change_backend:

             


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

from data_display import select_and_show_hetero_data,clean_display

with st.sidebar:
  module = st.radio('工程模块',['调控面板','环境参数','异构数据'])
  values = st.slider(
'选择时间段',
    min_value=datetime(times[0].year,times[0].month,times[0].day), 
    max_value=datetime(times[-1].year,times[-1].month,times[-1].day), 
    value=(datetime(times[30].year,times[30].month,times[30].day), 
            datetime(times[200].year,times[100].month,times[100].day))
    ,#step=datetime(year=2023,month=1,day=1,hour=1,minute=1),
    format="MM/DD")
    
  if st.button('Clear cache'):
    st.cache_data.clear()

if module == '环境参数':
    enviro_module()
elif module == '异构数据':
    clean_display()
elif module == '调控面板':
    control_pannel()

  