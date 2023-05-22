import streamlit as st 
import pandas as pd
import plotly.express as px


@st.cache_data
def show_everything(combine_df_s):

    f1,f2= st.columns((2,2),gap="medium")
    with f1:
        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['No. 1 area','No. 2 area','No. 3 area','No. 4 area','No. 5 area','No. 6 area','No. 7 area','No. 8 area','No. 9 area'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="植物表型像素",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15
                            ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['平均温度'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="温度",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['1号室内CO2浓度','2号室内CO2浓度'],height=300,template='plotly_dark')
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
        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['营养液EC'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="营养液EC",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['1号蓝比','2号蓝比','3号蓝比','1号绿比','2号绿比','3号绿比','1号红比','2号红比','3号红比'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="光谱",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['1号色温','2号色温','3号色温'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="色温",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)
        #st.area_chart(combine_df,x='顺序',y=['营养液EC'],height=300,use_container_width=True)
    with f2:
        fig = px.scatter(combine_df_s.diff(1),x=combine_df_s.index,y=['No. 1 area','No. 2 area','No. 3 area','No. 4 area','No. 5 area','No. 6 area','No. 7 area','No. 8 area','No. 9 area'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="植物表型像素差分",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15
                            ))
        st.plotly_chart(fig,use_container_width=True)
        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['平均湿度'],height=300,template='plotly_dark')
        fig.update_layout(title="湿度",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['营养液液温'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="营养液液温",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("""  ---  """)
        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['营养液PH'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="营养液PH",
                          legend_title_text=None,
                          font=dict(
            family="Serif",size=15
                          ))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['1号PPFD','2号PPFD','3号PPFD'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="PPFD",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(combine_df_s,x=combine_df_s.index,y=['1号PAR','2号PAR','3号PAR'],height=300,template='plotly_dark')
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None)
        fig.update_layout(title="PAR",
                            legend_title_text=None,
                            font=dict(
            family="Serif",size=15))
        st.plotly_chart(fig,use_container_width=True)

# Define a function that generates a list of time ranges for a period
def generate_time_ranges(start_time, end_time, own_freq, other_freq):
    time_ranges = []
    while start_time < end_time:
        time_ranges.append((start_time, start_time + own_freq))
        start_time += own_freq + other_freq
    return time_ranges

# Define the start and end times and frequency for each period
light_start_time = pd.Timestamp('2023-05-4 22:00:00')
light_end_time = pd.Timestamp('2023-05-21 22:00:00')    
light_frequency = pd.Timedelta(hours=24)
bug_freq = pd.Timedelta(hours=0)
dark_start_time = pd.Timestamp('2023-05-4 11:00:00')
dark_end_time = pd.Timestamp('2023-05-15 18:00:00')
dark_frequency = pd.Timedelta(hours=7)

#需要补充光质设定的信息，等查博消息

# Generate the time ranges for each period
light_time_ranges = generate_time_ranges(light_start_time, light_end_time, light_frequency,bug_freq)
dark_time_ranges = generate_time_ranges(dark_start_time, dark_end_time, dark_frequency, light_frequency)
#below i want a function that extract data starting from hetero, 
# using st.select to enable selecting the dataframe to see and show chart
def select_and_show_hetero_data():
    plants = pd.read_csv("./arranged_data4/Plant_data_halfhour.csv")
    whole_time=[pd.to_datetime(day+' '+hour) for day,hour in zip(plants['Date'],plants['Time'])]
    plants['time']=whole_time
    plants['pixel diff']=plants['Area per plant'].diff(1)
    plants=plants.set_index('time')
    plants['time'] = plants.index

    plants = plants[(plants.index.hour == 22) & (plants.index > '2023-05-01')]

    plants['time'] = [date.date() for date in plants.index.unique()]
    plants = plants.set_index('time')

    plants_day = pd.DataFrame({})
    #plants_day['time'] = plants.index.unique()
    #plants_day = plants_day.set_index('time')
    for i in range(1,10):
        new_df = pd.DataFrame({})
        new = []
        times =[]
        #print(i)
        for j in range(len(plants)):
            if plants['No.'][j] == i:
                new.append(plants['Area per plant'][j])
                times.append(plants.index[j])
        new_df['plant '+str(i)] = new
        new_df['plant '+str(i)+' diff'] = new_df['plant '+str(i)].diff(1)
        new_df['time'] = times
        #plants_day['time'] = plants.index.unique()
        #plants_day = plants_day.set_index('time')
        plants_day['No. '+str(i)+' area'] = new_df['plant '+str(i)]
    plants_day['time'] = new_df['time']
    plants_day = plants_day.set_index('time')

    import os 
    csv_path = "./arranged_data4"
    files = os.listdir(csv_path)
    num_files = len(files)-1
    dataframes4 = {}

    start = 44
    for i in range(num_files): #有效数据
        dataframes4['df'+str(i)] = pd.read_csv('arranged_data4/sub_df'+str(i)+'.csv')

    combine_df = dataframes4['df0']
    for i in range(start,num_files):
        combine_df=pd.concat((combine_df,dataframes4['df'+str(i)]))
    comb = combine_df
    enviros = comb
    comb['time'] = pd.to_datetime(comb['time'])
    day_enviros = {}
    day_means = {}

    for time_range in light_time_ranges:
        enviros_day = enviros[(enviros['time'] >= time_range[0]) & (enviros['time'] < time_range[1])]
        try:
            del enviros_day['Unnamed: 0']
            del enviros_day['Unnamed: 0.1']
        except:
            continue
        day_enviros[time_range[1].date()] = enviros_day
        day_means[time_range[1].date()] = enviros_day.mean()
    day_means = pd.DataFrame(day_means).transpose()
    test_hetero = pd.concat((plants_day,day_means))
    test_hetero['date'] = pd.to_datetime(test_hetero.index)
    
    test_hetero.sort_values(by='date',inplace=True)
    st.write(test_hetero)

    show_everything(test_hetero)