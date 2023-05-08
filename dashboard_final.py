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
    sample_im_selection = st.selectbox('植物生长',options=['im1','im2','im3'])
    st.image(sample_ims[sample_im_selection],caption=sample_im_selection,use_column_width=True)

    st.markdown("## 环境控制")
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

def show_everything(combine_df_s, mod_numero):
    try:
        del combine_df_s['Unnamed: 0']
        del combine_df_s['Unnamed: 0.1']
    except:
        pass
    f1,f2= st.columns((2,2),gap="medium")
    with f1:
        fig = px.line(combine_df_s,x='time',y=['plant ' + str(mod_numero)],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="植物表型像素",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15
                            ))
        st.plotly_chart(fig,use_container_width=True)

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
        fig = px.line(combine_df_s,x='time',y=['plant ' + str(mod_numero) + " diff"],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="植物表型像素差分",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15
                            ))
        st.plotly_chart(fig,use_container_width=True)
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
#below i want a function that extract data starting from hetero, 
# using st.select to enable selecting the dataframe to see and show chart
def select_and_show_hetero_data():
    heteros = []
    #heteros_dark = [] #暗期时
    #heteros_light = [] #光期时
    for i in range(1,10):
        df = pd.read_csv('./hetero_data/hetero_'+str(i)+'.csv')
        heteros.append(df[['plant ' + str(i),'plant ' + str(i) + ' diff','平均温度','平均湿度','1号CO2浓度','2号CO2浓度','1号蓝比','1号红比','1号绿比','1号PPFD','1号PAR']])
    #可以考虑表格展示每个dataframe在2号PAR这一列数值为零时的各参数的平均值
    #hetero_df = pd.DataFrame()
    selection = st.selectbox("选择模块", [i for i in range(1,10)])
    heteros[selection].time = pd.to_datetime(heteros[selection].time)
    combine_3h = heteros[selection].resample('3H', on='time').mean()
    three_h = st.expander("3小时平均值",expanded=True).table(combine_3h)
    with three_h:
        st.table(three_h)
    combine_1d = heteros[selection].resample('1D', on='time').mean()
    one_d = st.expander("1天平均值",expanded=True)
    with one_d:
        st.table(combine_1d)
    
    show_everything(heteros[selection],selection)

def emist_ai():
    from sko.GA import GA
    from scipy.optimize import curve_fit
    from ac_models import standard_capacity, integral_controller
    import sys 
    sys.path.append('/Users/wuzhenxiong/主营科研/红宝石项目/23年三月份整合/stat_mod_sim')
    from scores import scores
    df = s_df
    xdata_T = df['空调手动模式选择'][:-1],df['空调风速选择'][:-1], df['户外温度'][:-1], df['平均温度'][:-1],df['空调手动温度设定'][:-1], df['灯具负荷'][:-1],df['自然负荷'][:-1],df['新风负荷'][:-1]

    T_params, T_covs = curve_fit(standard_capacity, xdata_T, df['平均温度'][1:], 
                                p0=np.concatenate([[0.1 for i in range(5)] for i in range(8)]),
                                #bounds=(),
                                )
    
    df_scores = pd.DataFrame({})
    r2s = []
    rmse = []
    mape = []
    for key in df_dict:
        df = df_dict[key]
        xdata_T = df['空调手动模式选择'][:-1],df['空调风速选择'][:-1], df['户外温度'][:-1], df['平均温度'][:-1], df['空调手动温度设定'][:-1],df['灯具负荷'][:-1],df['自然负荷'][:-1],df['新风负荷'][:-1]
        fit = standard_capacity(xdata_T, *T_params)
        real = df['平均温度'][1:]
        results = scores(fit,real)
        #r2s.append(str(round(results[0][0]*100,2)) + ' %')
        r2s.append(round(results[0][0]*100,2))
        rmse.append(results[1][0])
        mape.append(results[2][0])
    df_scores['dataset'] = list(df_dict.keys())
    df_scores['R2'] = r2s
    df_scores['RMSE'] = rmse 
    df_scores['MAPE'] = mape
    #st.table(df_scores)

    #start_sim=st.button('AI热特性识别')
    #if start_sim:
    st.subheader('温度仿真精度')
    fig = px.bar(df_scores,x='dataset',y=['R2'],color='RMSE',color_discrete_sequence=px.colors.sequential.Plasma_r)
    st.plotly_chart(fig,use_container_width=True)
    #st.table(df_scores)
    
    #start_control = st.button('AI温度调控')
    #if start_control:
    controller = integral_controller()
    st.subheader('温度控制')
    #col1,col2 = st.columns(2)
    #with col1:
    controller.predicted_load = df['总热渗入量'][:200]
    col1, col2 = st.columns(2)
    with col1:
        controller.obj_T = st.slider('目标温度',min_value=float(18),max_value=float(25),value=float(22),step=0.1)
        controller.T_params = T_params
        controller.outdoor_T = st.slider('室外温度',min_value=float(1),max_value=float(25),value=float(12),step=0.1)
        controller.current_T = st.slider('当前温度',min_value=float(15),max_value=float(30),value=float(24),step=0.1)
        start_optimize = st.button('开始优化调控')
        st.write('调节时长-运行模式-风速档位')
    with col2:
        #start_optimize = st.button('开始优化调控')
        #st.write('调节时长-运行模式-风速档位')

        if start_optimize:
            optimizer = GA(
            func=controller.optimal_load,
            n_dim=3,
            lb=[1,1,1],
            ub=[30,4,7],
            #constraint_eq=eq_cstr,
            precision=1
            )
            x,y=optimizer.run()

            st.metric('调控时长',value=str(int(x[0])) + ' 分钟' )
            st.metric('运行模式',value=x[1])
            st.metric('风速档位',value=x[2])
            #st.write(controller.thermal_demand)
            st.metric('达标率',value=str(round(100*(1-abs(y[0]/controller.thermal_demand)),1)) + ' %')

    st.subheader('咨询顾问AI')
    components.iframe(
"https://getcody.ai/widget/29383a77-71ed-4bdd-84f2-181530904ef2",
height=1000,
width=1000,scrolling=True
                )

with st.sidebar:
  module = st.radio('工程模块',['环境参数','异构数据','能源AI','设备全景'])
  values = st.slider(
'选择时间段',
    min_value=datetime(times[0].year,times[0].month,times[0].day), 
    max_value=datetime(times[-1].year,times[-1].month,times[-1].day), 
    value=(datetime(times[30].year,times[30].month,times[30].day), 
            datetime(times[200].year,times[100].month,times[100].day))
    ,#step=datetime(year=2023,month=1,day=1,hour=1,minute=1),
    format="MM/DD")
if module == '环境参数':
    enviro_module()
elif module == '异构数据':
    select_and_show_hetero_data()
elif module == '能源AI':
    emist_ai()
  