import pandas as pd 
from led_models import modules_control,round_1_led
import time
import numpy as np

def data_pretreatment(df_number,df):

    #df = pd.read_csv('dataframe'+str(df_number)+'.csv')
    df['平均温度']=(df['1号室内温度']+df['2号室内温度'])/2
    df['平均湿度']=(df['1号室内湿度']+df['2号室内湿度'])/2
    df['time'] = pd.to_datetime(df['time'])
    standard_lights_power, standard_lights_heat = round_1_led()
    led_heat = []
    for i in range(len(df)):
        if df['1号PPFD'][i]<1:
            led_heat.append(0)
        else:
            led_heat.append(standard_lights_heat/1000)
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
            print(i)
            for j in range(len(plants)):
                if plants['No.'][j] == i:
                    new.append(plants['Area per plant'][j])
                    times.append(plants['time'][j])
            new_df['plant '+str(i)] = new
            new_df['plant '+str(i)+' diff'] = new_df['plant '+str(i)].diff(1)
            new_df['time'] = times 
            new_df['time'] = pd.to_datetime(new_df['time'])
            #new_df = new_df.set_index('time')
            #new_df.index = pd.to_datetime(new_df.index)
            #ew_df = new_df.resample('30m').mean()
            try:
                #new_df.resample('1H').mean()
                df_collection.append(new_df)
            except:
                pass

        dataframes4 = {}
        for i in range(33): #有效数据
            dataframes4['df'+str(i)] = pd.read_csv('vertical_farm_dp/arranged_data4/sub_df'+str(i)+'.csv')
        
        combine_df = dataframes4['df10']
        for i in range(11,33):
            combine_df=pd.concat([combine_df,dataframes4['df'+str(i)]],axis=1)

        merged_df = combine_df
        for i in range(len(df_collection)):
            #print(i)
            merged_df = pd.merge_asof(merged_df,df_collection[i],on='time')
            #merged_df['plant ' + str(i+1) + ' diff'] = merged_df['plant '+str(i+1)].diff(1)
        merged_df = merged_df.set_index('time')#每分钟数据
        daily_df = merged_df.resample('1800s').mean()#半小时数据

        hetero_collection = []
        #每一排都弄一波数据
        for i in range(1,10):
            condition = (daily_df['plant ' + str(i) + ' diff']>0)
            daily_df[condition].to_csv('hetero_'+str(i)+'.csv')

        import subprocess

        # Path to your Git repository
        repo_path = 'ThomasXIONG151215/vertical_farm_dp'

        # Add all files to the git repository
        subprocess.run(['git', 'add', '.'], cwd=repo_path)

        # Commit changes with a commit message
        commit_message = 'Update Data'
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path)

        # Push changes to the remote repository
        subprocess.run(['git', 'push'], cwd=repo_path)
        print('pushed')
        time.sleep(30*60)
        #git commit
        #git push
