import streamlit as st

def analyze_growth_performance(df):
    result = {}
    
    for column in df.columns:
        if column.startswith('表型'):
            # 计算表型的增长幅度
            growth_rate = df[column].diff().mean()
            
            # 计算表型的最大值和最小值
            max_value = df[column].max()
            min_value = df[column].min()
            
            # 计算表型的平均值和标准差
            mean_value = df[column].mean()
            std_value = df[column].std()
            
            # 构建结果字典
            result[column] = {
                '增长幅度': growth_rate,
                '最大值': max_value,
                '最小值': min_value,
                '平均值': mean_value,
                '标准差': std_value
            }
    
    return result

def all_performance(df):
    result = {}
    
    for column in df.columns:
        #if column.startswith('表型'):
        # 计算增长幅度
        growth_rate = df[column].diff().mean()
        
        # 计算最大值和最小值
        max_value = df[column].max()
        min_value = df[column].min()
        
        # 计算平均值和标准差
        mean_value = df[column].mean()
        std_value = df[column].std()
        
        # 构建结果字典
        result[column] = {
            '变化幅度': growth_rate,
            '最大值': max_value,
            '最小值': min_value,
            '平均值': mean_value,
            '标准差': std_value
        }
    
    return result

def get_best_combination(query):
    # 计算变化最多的时间段
    max_change = st.session_state.df['表型1'].diff().abs().max()
    max_change_index = st.session_state.df['表型'].diff().abs().idxmax()
    max_change_period = st.session_state.df.loc[max_change_index, '时间']

    # 获取该时间段的相关信息
    temperature = st.session_state.df.loc[max_change_index, '温度']
    humidity = st.session_state.df.loc[max_change_index, '湿度']
    light_intensity = st.session_state.df.loc[max_change_index, '光质强度']
    ph_value = st.session_state.df.loc[max_change_index, 'pH']
    ec_value = st.session_state.df.loc[max_change_index, 'EC']
    light_period = st.session_state.df.loc[max_change_index, '光周期']

    # 生成结果字符串
    result = f"表型在温度{temperature}，湿度{humidity}，光质强度{light_intensity}，pH{ph_value}，EC{ec_value}，光周期{light_period}的{max_change_period}变化最多，变化幅度为{max_change}。"
    return result

#st.info(get_best_combination("最近的表型变化最大的时间段是什么时候？"),icon="🤖")

def calculate_average_change_around_value(column_name, specific_value):
    # 计算上下限
    上限 = specific_value + (0.05 * specific_value)
    下限 = specific_value - (0.05 * specific_value)
    
    # 获取特定范围内的数据
    subset = st.session_state.df[(st.session_state.df[column_name] >= 下限) & (st.session_state.df[column_name] <= 上限)]
    
    # 计算表型的变化
    表型变化 = subset['表型差值']#.diff().abs()
    if len(表型变化)>0:
    # 计算平均变化值
        平均变化 = 表型变化.mean()
    else:
        平均变化 = None
    return 平均变化