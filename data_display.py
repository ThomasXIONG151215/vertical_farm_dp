import streamlit as st 
import pandas as pd
import plotly.express as px

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

        fig = px.line(combine_df_s,x='time',y=['平均温度'],height=300,template='plotly_dark')
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
        fig = px.line(combine_df_s,x='time',y=['平均湿度'],height=300,template='plotly_dark')
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
    heteros_daily = []
    heteros_3H = []
    heteros_30min = []

    for i in range(1,10):
        daily_df = pd.read_csv('./hetero_data/daily_hetero_'+str(i)+'.csv')
        three_h_df = pd.read_csv('./hetero_data/3H_hetero_'+str(i)+'.csv')
        thirty_min_df = pd.read_csv('./hetero_data/30min_hetero_'+str(i)+'.csv')
        parameters = ['time','plant ' + str(i),'plant ' + str(i) + ' diff','平均温度','平均湿度',
                      '1号室内CO2浓度','2号室内CO2浓度','营养液EC','营养液PH','营养液液温',
                      '1号蓝比','1号红比','1号绿比','1号PPFD','1号PAR','2号蓝比','2号红比',
                      '2号绿比','2号PPFD','2号PAR','3号蓝比','3号红比','3号绿比','3号PPFD','3号PAR','1号色温','2号色温','3号色温']
        heteros_daily.append(daily_df[parameters])
        heteros_3H.append(three_h_df[parameters])
        heteros_30min.append(thirty_min_df[parameters])
    #可以考虑表格展示每个dataframe在2号PAR这一列数值为零时的各参数的平均值
    #hetero_df = pd.DataFrame()
    selection = st.selectbox("选择模块", [i for i in range(1,10)])
    
    combine_1d = heteros_daily[selection-1]
    #combine_1d['time'] = combine_1d.index
    one_d = st.expander("1天平均值",expanded=True)
    with one_d:
        st.dataframe(combine_1d)
        show_everything(combine_1d,selection)
    combine_3h = heteros_3H[selection-1]
    #combine_3h['time'] = combine_3h.index
    three_h = st.expander("3小时平均值",expanded=True)
    with three_h:
        st.dataframe(combine_3h)
        show_everything(combine_3h,selection)

    combine_30m = heteros_3H[selection-1]
    #combine_30m['time'] = combine_30m.index
    three_h = st.expander("30分钟平均值",expanded=True)
    with three_h:
        st.dataframe(combine_30m)
        show_everything(combine_30m,selection)