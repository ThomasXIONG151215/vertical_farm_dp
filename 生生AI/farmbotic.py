import pandas as pd
import random
import streamlit as st 
from streamlit_chat import message
from analysis_tools import analyze_growth_performance, all_performance,get_best_combination,calculate_average_change_around_value
from agent_build import read_pdf_and_store_memory,csv_agent,prompt_llm_chain_agent_executor

st.title("生生AI")
# 创建时间范围
start_time = pd.Timestamp('2023-06-18 00:00:00')
end_time = start_time + pd.DateOffset(hours=719)

# 生成时间索引
time_index = pd.date_range(start=start_time, end=end_time, freq='12H')


data_generation = """
# 生成随机数据
data = {
    '时间': time_index,
    '表型': range(0, len(time_index)),
    '温度': [],
    '湿度': [random.randint(50, 70) for _ in range(len(time_index))],
    '光质强度': [random.randint(3000, 4000) for _ in range(len(time_index))],
    'pH': [round(random.uniform(5.0, 6.5), 1) for _ in range(len(time_index))],
    'EC': [round(random.uniform(1.0, 2.5), 1) for _ in range(len(time_index))],
    '光周期': random.choice([('16-8', '18-6')]) * ((len(time_index) // 2)),
    'CO2浓度': [round(random.uniform(400, 800), 1) for _ in range(len(time_index))]
}

# 根据时间段设置温度
for timestamp in time_index:
    hour = timestamp.hour
    if 6 <= hour <= 18:
        temperature = round(random.uniform(23.5, 24.5), 1)
    else:
        temperature = round(random.uniform(21.5, 22.5), 1)
    data['温度'].append(temperature)

# 生成其他随机的表型列和对应的光质强度和光周期
num_additional_columns = random.randint(5, 7)
for i in range(num_additional_columns):
    column_name = f'表型{i+1}'
    data[column_name] = [random.randint(0, len(time_index)) for _ in range(len(time_index))]
    data[f'光质强度{i+1}'] = [random.randint(3000, 4000) for _ in range(len(time_index))]
    data[f'光周期{i+1}'] = random.choice([('16-8', '18-6')]) * ((len(time_index) // 2))

# 创建数据框
st.session_state.df = pd.DataFrame(data)
st.session_state.df.to_csv('sample_df.csv')
"""

st.session_state.df = pd.read_csv('sample_df.csv')


# 调用函数进行分析
growth_analysis = analyze_growth_performance(st.session_state.df)
st.session_state.df['表型差值'] = st.session_state.df['表型'].diff().abs()

# 转换为DataFrame
df_analysis = pd.DataFrame(growth_analysis)

def analysis_to_pdf():
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_font('SIMYOU','','ttf/SIMYOU.TTF',uni=True)
    pdf.set_font('SIMYOU',size=10)
    pdf.add_page()
    #pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, '你好 World!')

    pdf.output('tuto1.pdf', 'F')


# 使用示例
value = 25  # 替换为您想要的特定值
col = '温度'  # 替换为您想要的列名
unit = '度'

param_units = {
    '温度':'度',
    '湿度':'%',
    'CO2浓度':'ppm',
    '光质强度':'%',
    'pH':None,
    'EC':None,
    #'光周期':None
}

param_range = {
    '温度':(15,35),
    '湿度':(30,90),
    'CO2浓度':(300,1500),
    '光质强度':(0,100),
    'pH':(5,7),
    'EC':(0,3),
    #'光周期':(0,24)
}

import plotly.express as px

tab1, tab2 = st.tabs(["统计分析", "知识问答"])
with tab1:
    #st.write("## 数据查看")
    with st.expander("整体数据"):
        try:
            del st.session_state.df['Unnamed: 0']
        except:
            pass
        st.dataframe(st.session_state.df,use_container_width=True)
    
    #一一对应关系
    # 计算相关性
    st.write("## 相关性分析")
    #choices = st.multiselect("选择参数", st.session_state.df.columns,['温度','湿度','CO2浓度','光质强度','pH','EC','光周期'])
    #if st.button("计算相关性"):
    correlation = st.session_state.df.corr(method='kendall')#[choices].corr()

    # 使用Plotly库创建相关性矩阵图表
    fig = px.imshow(correlation)

    # 设置图表标题和轴标签
    fig.update_layout(
        title="参数相关性",
        xaxis_title="参数",
        yaxis_title="参数"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("## 表型分析")
    with st.expander("表型分析结果"):
        st.dataframe(df_analysis,use_container_width=True)
        st.info(get_best_combination("最近的表型变化最大的时间段是什么时候？"),icon="🌱")

    st.button("输出分析报告",on_click=analysis_to_pdf)
    col1, col2 = st.columns(2)
    with col1:
        param_check = st.selectbox('选择参数', options=list(param_units.keys()))
        #st.write((param_range[param_check][0]+param_range[param_check][1])/2)
        
    with col2:
        pivot = st.slider(f'选择{param_check}', min_value=param_range[param_check][0], max_value=param_range[param_check][1], step=1)
        av_diff = calculate_average_change_around_value(param_check, pivot)
        unit = param_units[param_check]
        #av_25_T = calculate_average_change_around_value(st.session_state.df, col, value)

        if av_diff is not None:
            #st.write(f"在{param_check}在{pivot}{unit}左右(上下波动不超过5%)，表型的平均变化值为{av_diff}。")
            message(f"在{param_check}在{pivot}{unit}左右(上下波动不超过5%)，表型的平均变化值为{av_diff}。", is_user=False)    
        else:
            #st.write(f"没有过{param_check}在{pivot}{unit}左右的情况。")
            message(f"没有过{param_check}在{pivot}{unit}左右的情况。", is_user=False)
    


    #st.write("## 数据集助手")
    #from memory_build import entity_memory_conversation
    #data_assistant = entity_memory_conversation()
    #st.write(data_assistant.memory.entity_store.store)
    #st.write(data_assistant.predict(input="What is your name"))
    #prompt_llm_chain_agent_executor()
    #csv_agent('sample_df.csv')


with tab2:
    st.write('## 知识问答') #关于pdf文档知识问答
    read_pdf_and_store_memory()
    