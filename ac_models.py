import numpy as np 

def RLC_T(xdata, alpha, reverse_Cr, reverse_R_wall,reverse_R_neighbor, L_neighbor): #单个区间的时间内 内部区块之间的热交互对温度产生的影响
  # RLC温度模型
  # 模型输入：当下温度，近邻温度，室外温度, 净得热量(热渗入量-制冷量) kW ，近邻热渗入量变化kW，近邻相对湿度变化
  # 模型系数：制冷分布，1/空间热容，1/近邻热阻，近邻朝向对象空间的热感

  tho = 60#s

  object_T_now, neighbor_T, outdoor_T, I_net, I_diff_neighbor, RH_diff_neighbor = xdata 
  #当前时刻的，预测下一时刻的

  #I_net = I_input + I_system #冷量是负数 kW
  T_diff_object_neighbor = neighbor_T - object_T_now
  T_diff_object_outdoor = outdoor_T - object_T_now

  X =  alpha * I_net + reverse_R_wall * T_diff_object_outdoor + reverse_R_neighbor * ( T_diff_object_neighbor + tho * I_diff_neighbor * RH_diff_neighbor * L_neighbor )
  #X里头的第二项self.tho出现了两次是为了保证让近邻开放空间的互热感单位保持一致
  #alpha=空调输出在空间的分布系数｜ 冷扩散率/(空间面积*60秒时间）

  new_T = object_T_now + reverse_Cr * tho * X

  return new_T

import pandas as pd



def standard_capacity(xdata,*args): #每分钟性能
    #空调对整体温度与湿度的影响 -> 主要专注于定量空调性能, 这是一个末端对两个分区的情形 -> 往后再延伸到分区之间的交互，去定义它们各自的热交互及热损失
    mode,intensity, outdoor_X, object_X,set_X, light, nature, fresh  = xdata
    thermal_capacitance = args[0] #最初的一个是热容
    light_coef=args[1]
    natural_coef=args[2]
    fresh_coef=args[3]
    #[light, nature, fresh] = other_inputs
    args = args[5:]#后面几个都是空调不同模式的

    split = int(len(args)/8) #自动,制冷，送风，制热，除湿
    auto_params = args[:split]
    cooling_params = args[split:2*split] #四个系数同时用来定义输出(扩散+损失)
    wind_params = args[2*split:3*split]
    heating_params = args[3*split:4*split]
    dehumid_params = args[4*split:5*split]
    radiant_params = args[5*split:6*split]
    quick_params = args[6*split:7*split]
    large_params = args[7*split:]
    '''
    =0自动
    =1制冷
    =2抽湿
    =3送风
    =4制热
    =6地暖
    =7快热
    =8供暖
    '''

    mode_dict = {
      0: auto_params,
      1: cooling_params,
      2: dehumid_params,
      3: wind_params,
      4: heating_params,
      6: radiant_params,
      7: quick_params,
      8: large_params
    }
    #print(mode_dict)
    if isinstance(mode,int) or isinstance(mode,float):
      mode = int(mode)
      #print('int')
      mode_params = {
          'a': mode_dict[mode][0],
          'b': mode_dict[mode][1],
          'c': mode_dict[mode][2],
          'd': mode_dict[mode][3],
          #'e': mode_dict[mode][0],
      }
    else:
      #print('frame')
      mode_params = pd.DataFrame({
        'a':[mode_dict[i][0] for i in mode],
        'b':[mode_dict[i][1] for i in mode],
        'c':[mode_dict[i][2] for i in mode],
        'd':[mode_dict[i][3] for i in mode],
        #'e':[mode_dict[i][4] for i in mode]
      })
      #[mode_dict[i] for i in mode]

    ac_X = intensity#*(set_X-object_X) #* outdoor_X

    ac_capacity = mode_params['a'] + ac_X * mode_params['b'] + ac_X ** 2 * mode_params['c'] + ac_X ** 3 * mode_params['d']

    new_X = object_X + (ac_capacity + light_coef*light+natural_coef*nature+fresh_coef*fresh) * 60 * thermal_capacitance#* mode_params['e'] 
    
    #一分钟千焦热量 #ac输出是与其它冷热源输出相加关系
    
    return new_X


def n_standard_capacity(xdata,*args): #每分钟性能
    #空调对整体温度与湿度的影响 -> 主要专注于定量空调性能, 这是一个末端对两个分区的情形 -> 往后再延伸到分区之间的交互，去定义它们各自的热交互及热损失
    N, mode,intensity, outdoor_X, object_X,set_X, light, nature, fresh  = xdata
    thermal_capacitance = args[0] #最初的一个是热容
    light_coef=args[1]
    natural_coef=args[2]
    fresh_coef=args[3]
    #[light, nature, fresh] = other_inputs
    args = args[5:]#后面几个都是空调不同模式的

    split = int(len(args)/8) #自动,制冷，送风，制热，除湿
    auto_params = args[:split]
    cooling_params = args[split:2*split] #四个系数同时用来定义输出(扩散+损失)
    wind_params = args[2*split:3*split]
    heating_params = args[3*split:4*split]
    dehumid_params = args[4*split:5*split]
    radiant_params = args[5*split:6*split]
    quick_params = args[6*split:7*split]
    large_params = args[7*split:]
    '''
    =0自动
    =1制冷
    =2抽湿
    =3送风
    =4制热
    =6地暖
    =7快热
    =8供暖
    '''

    mode_dict = {
      0: auto_params,
      1: cooling_params,
      2: dehumid_params,
      3: wind_params,
      4: heating_params,
      6: radiant_params,
      7: quick_params,
      8: large_params
    }
    #print(mode_dict)
    if isinstance(mode,int) or isinstance(mode,float):
      mode = int(mode)
      #print('int')
      mode_params = {
          'a': mode_dict[mode][0],
          'b': mode_dict[mode][1],
          'c': mode_dict[mode][2],
          'd': mode_dict[mode][3],
          #'e': mode_dict[mode][0],
      }
    else:
      #print('frame')
      mode_params = pd.DataFrame({
        'a':[mode_dict[i][0] for i in mode],
        'b':[mode_dict[i][1] for i in mode],
        'c':[mode_dict[i][2] for i in mode],
        'd':[mode_dict[i][3] for i in mode],
        #'e':[mode_dict[i][4] for i in mode]
      })
      #[mode_dict[i] for i in mode]

    ac_X = intensity#*(set_X-object_X) #* outdoor_X

    ac_capacity = mode_params['a'] + ac_X * mode_params['b'] + ac_X ** 2 * mode_params['c'] + ac_X ** 3 * mode_params['d']

    new_X = object_X + (ac_capacity + light_coef*light+natural_coef*nature+fresh_coef*fresh) * N * 60 * thermal_capacitance#* mode_params['e'] 
    
    #一分钟千焦热量 #ac输出是与其它冷热源输出相加关系
    
    return new_X

def thermal_demand(xdata,*args):
    N, diff_X,lights,naturals,freshes  = xdata #diff_X指的是 目标温度-当前温度
    thermal_capacitance = args[0] #最初的一个是热容

    #new_X = object_X + (ac_capacity + other_inputs) * 60 * thermal_capacitance#* mode_params['e'] 
    
    #假设的是，后面N分钟后都是同样或者差不多的热渗入了情况(灯+自然被卷进来的循环风+新风机强制照进来的新风)
    
    actual_load = diff_X / (N*60*thermal_capacitance) - args[1]*lights + args[2]*naturals + args[3]*freshes

    return actual_load


def capacity_cost(xdata,*args): #每分钟性能
    #空调对整体温度与湿度的影响 -> 主要专注于定量空调性能, 这是一个末端对两个分区的情形 -> 往后再延伸到分区之间的交互，去定义它们各自的热交互及热损失
    mode,intensity, outdoor_X, object_X,set_X, light, nature, fresh  = xdata
    #thermal_capacitance = args[0] #最初的一个是热容
    #fresh_fan_params = args[1:5] #前四个同样是输出分析，
  
    args = args[5:]#后面几个都是空调不同模式的

    split = int(len(args)/8) #自动,制冷，送风，制热，除湿
    auto_params = args[:split]
    cooling_params = args[split:2*split] #四个系数同时用来定义输出(扩散+损失)
    wind_params = args[2*split:3*split]
    heating_params = args[3*split:4*split]
    dehumid_params = args[4*split:5*split]
    radiant_params = args[5*split:6*split]
    quick_params = args[6*split:7*split]
    large_params = args[7*split:]
    '''
    =0自动
    =1制冷
    =2抽湿
    =3送风
    =4制热
    =6地暖
    =7快热
    =8供暖
    '''

    mode_dict = {
      0: auto_params,
      1: cooling_params,
      2: dehumid_params,
      3: wind_params,
      4: heating_params,
      6: radiant_params,
      7: quick_params,
      8: large_params
    }
    #print(mode_dict)
    if isinstance(mode,int) or isinstance(mode,float):
      mode = int(mode)
      #print('int')
      mode_params = {
          'a': mode_dict[mode][0],
          'b': mode_dict[mode][1],
          'c': mode_dict[mode][2],
          'd': mode_dict[mode][3],
          #'e': mode_dict[mode][0],
      }
    else:
      #print('frame')
      mode_params = pd.DataFrame({
        'a':[mode_dict[i][0] for i in mode],
        'b':[mode_dict[i][1] for i in mode],
        'c':[mode_dict[i][2] for i in mode],
        'd':[mode_dict[i][3] for i in mode],
        #'e':[mode_dict[i][4] for i in mode]
      })

    ac_X = intensity#*(set_X-object_X) #* outdoor_X
    #fan_X = (100-fan_openness) * (outdoor_X - object_X) #

    ac_capacity = mode_params['a'] + ac_X * mode_params['b'] + ac_X ** 2 * mode_params['c'] + ac_X ** 3 * mode_params['d']
    #fan_capacity = fresh_fan_params[0] + fan_X * fresh_fan_params[1] + fan_X ** 2 * fresh_fan_params[2] + fan_X ** 3 * fresh_fan_params[3]
    
    return -ac_capacity #+ fan_capacity #kW


class integral_controller():
  
  def __init__(self):
    pass
      
  def optimal_load(self,control_x):
    [N,mode,intensity,set_T] = control_x
    self.diff = self.obj_T - self.current_T #obj T是目标，set T是设定/设定值用来调节压缩机转速
    N = int(N)
    #N->预测N分钟后的平均热量水平
    self.light_sums = np.sum(self.predicted_lights[:N])/N
    self.natural_sums = np.sum(self.predicted_naturals[:N])/N
    self.fresh_sums = np.sum(self.predicted_freshes[:N])/N
    

    load_xdata = N, self.diff, self.light_sums, self.natural_sums, self.fresh_sums
    self.thermal_demand = thermal_demand(load_xdata, *self.T_params)
    #obj_T
    #T_params
    #self.outdoor_T, #current_T #other_heat_inputs
    integral_x = mode,intensity,self.outdoor_T, self.current_T, set_T, self.light_sums, self.natural_sums, self.fresh_sums
    #eq_cstr = [
    #  lambda x: standard_capacity - self.obj_X
    #]

    output = capacity_cost(
      integral_x,
      *self.T_params
    )

    return abs(output - self.thermal_demand)

