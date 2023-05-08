import pandas as pd 
from led_models import modules_control,round_1_led,light_module
import time
import numpy as np

start_time_1 = pd.to_datetime('2023-03-31')
end_time_1 = pd.to_datetime('2023-04-10')
start_time_2 = pd.to_datetime('2023-04-10')
end_time_2 = pd.to_datetime('2023-04-27')
#光质设定表：颜色+涉及时段
set_table_1 = pd.DataFrame({})
set_table_1['R'] = [10,13,32,28,12,35,32,13,24]
set_table_1['FR'] = [0,0,0,0,0,0,0,0,0]
set_table_1['B'] = [0,0,10,19,0,13,21,0,10]
set_table_1['W'] = [10,14,0,0,12,0,0,10,0]
hours_18 = [16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9]

set_table_1['hours'] = [hours_18,hours_18,hours_18,hours_18,hours_18,hours_18,hours_18,hours_18,hours_18]

set_table_2 = pd.DataFrame({})
set_table_2['R'] = [10,0,22,22,0,22,22,0,24]
set_table_2['FR'] = [0,0,0,0,0,0,0,0,0]
set_table_2['B'] = [0,0,10,10,0,10,10,0,10]
set_table_2['W'] = [10,14,0,0,14,0,0,14,0]

set_table_2['hours'] = [hours_18[:-3],hours_18[:-6],hours_18,hours_18[:-3],hours_18[:-3],hours_18,hours_18[:-3],hours_18,hours_18[:-3]]


def data_pretreatment(df_number,df):

    #df = pd.read_csv('dataframe'+str(df_number)+'.csv')
    df['平均温度']=(df['1号室内温度']+df['2号室内温度'])/2
    df['平均湿度']=(df['1号室内湿度']+df['2号室内湿度'])/2
    df['time'] = pd.to_datetime(df['time'])
    led_heat = []
    for i in range(len(df)):
        if df['time'][i] >= start_time_1 and df['time'][i] < end_time_1:
            set_table = set_table_1
        elif df['time'][i] >= start_time_1 and df['time'][i] < end_time_1:
            set_table = set_table_2
        total_heat = 0
        for md in range(9):
            if df['time'][i] in set_table['hours'][md]:
                light_heat = light_module(white=set_table['W'][md],
                                      blue=set_table['B'][md],
                                      red_1=set_table['FR'][md],
                                      red_2=set_table['R'][md])
                total_heat += light_heat
            else:
                pass 
        led_heat.append(total_heat)
    df['灯具负荷'] = led_heat #kW
    df['自然负荷'] = (df['户外温度'] - df['平均温度']) * 1.1 * 0.5 * 1.005 * 1.29 #kW #循环风机自然进热#循环风机要一直开所以一直有热量进入
    df['新风负荷'] = (110-df['新风机手动开度'])/100 * (df['户外温度'] - df['平均温度']) * 0.5 * 1.005 * 1.29
    df['总热渗入量'] = df['灯具负荷']+df['自然负荷']+df['新风负荷']
    freq = pd.to_timedelta(np.diff(df.time).min())
    freq = 5 * freq
    grouper = df['time'].diff().gt(freq).cumsum()
    #grouped = [x for _,x in df.groupby(grouper)]
    for _,x in df.groupby(grouper):
        x.to_csv('vertical_farm_dp/arranged_data'+str(df_number)+'/sub_df' + str(_) + '.csv')

if __name__ == "__main__":
    while True:
        df = pd.read_csv("G:\生生不息\实验数据\BaiduSyncdisk\dataframe4.csv")
        data_pretreatment(4,df)

        plants = pd.read_csv("G:\生生不息\实验数据\BaiduSyncdisk\Plant_data_halfhour.csv")
        whole_time=[pd.to_datetime(day+' '+hour) for day,hour in zip(plants['Date'],plants['Time'])]
        plants['time']=whole_time
        plants['pixel diff']=plants['Area per plant'].diff(1)
        plants=plants.set_index('time')
        plants['time'] = plants.index
        #plants = plants[:-1]
        re_arranged_plants = pd.DataFrame({})
        df_collection = []

        for i in range(1,10):
            new_df = pd.DataFrame({})
            new = []
            times = []
            #print(i)
            for j in range(len(plants)):
                if plants['No.'][j] == i:
                    new.append(plants['Area per plant'][j])
                    times.append(plants['time'][j])
            new_df['plant '+str(i)] = new
            new_df['plant '+str(i)+' diff'] = new_df['plant '+str(i)].diff(1)
            new_df['time'] = times 
            new_df['time'] = pd.to_datetime(new_df['time'])

            try:
                #new_df.resample('1H').mean()
                df_collection.append(new_df)
            except:
                pass

        import os 

        dataframes4 = {}
        csv_path = "vertical_farm_dp/arranged_data4"
        files = os.listdir(csv_path)
        num_files = len(files)
        print(num_files)
        for i in range(num_files):
            dataframes4['df'+str(i)] = pd.read_csv("vertical_farm_dp/arranged_data4/sub_df"+str(i)+".csv")

        combine_df = pd.concat([dataframes4[key] for key in dataframes4.keys()],ignore_index=True)

        merged_df = combine_df
        merged_df['time'] = pd.to_datetime(merged_df['time'])
        for i in range(len(df_collection)):
            print(i)
            df_collection[i]['time'] = pd.to_datetime(df_collection[i]['time'])
            merged_df = pd.merge_asof(merged_df,df_collection[i],on='time',direction='nearest')
        merged_df = merged_df.set_index('time')
        daily_df = merged_df.resample('1D').mean()#1天数据
        three_hour_df = merged_df.resample('3H').mean()#3小时数据
        half_hour_df = merged_df.resample('30min').mean()#半小时数据

        hetero_collection = []
        #每一排都弄一波数据
        for i in range(1,10):
            daily_condition = (daily_df['plant ' + str(i) + ' diff']>0)
            three_hour_condition = (three_hour_df['plant ' + str(i) + ' diff']>0)
            half_hour_condition = (half_hour_df['plant ' + str(i) + ' diff']>0)
            daily_df[daily_condition].to_csv('vertical_farm_dp/hetero_data/daily_hetero_'+str(i)+'.csv')
            three_hour_df[three_hour_condition].to_csv('vertical_farm_dp/hetero_data/3H_hetero_'+str(i)+'.csv')
            half_hour_df[half_hour_condition].to_csv('vertical_farm_dp/hetero_data/30min_hetero_'+str(i)+'.csv')

        time.sleep(30*60)