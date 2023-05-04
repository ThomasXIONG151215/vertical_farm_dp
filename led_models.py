import numpy as np 

def light_module(white, blue, red_1, red_2):
  white_part = 300 * white/100
  blue_part = 110 * blue/100
  red_1_part = 100 * red_1/100
  red_2_part = 240 * red_2/100

  total_power = white_part + blue_part + red_1_part + red_2_part
  
  return total_power #以后可以比对功率和散热量的关系, 可以按照0.45统计



def modules_control(whites, blues, reds_1, reds_2): #九个模块

  modules_power = 0 #W
  modules_heat = 0#W 假设效率为0.4

  for w, b, r1, r2 in zip(whites, blues, reds_1, reds_2):
    modules_power += light_module(w,b,r1,r2)
  
  modules_heat = 0.4 * modules_power

  return modules_power, modules_heat

def round_1_led():
  nine_modules = [229,273,222,265,159,197,160,200,222]

  return np.sum(nine_modules), np.sum(nine_modules)*0.4 #power in W, heat dissipation in W