# -*- coding: utf-8 -*-
"""STC_APP_Test_Scriptv5

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nz_MGqPs5z1rz_G6NBl8xH-dQJxeK1Z3 : Private
    Author : Hamza Qureshi

DESCRIPTION
This code include following :
1. Create demo data dynamic method
2. Generate all parameters added by user from Application[Working Fine]
3. Get input file
4. Create 2 CSV or Text files [data and laser] both
"""
  
#!pip install pycryptodome
#you can use requirements.txt
from typing import Optional, List, Dict, Any, Tuple
from global_parameters import PARAMETERS,DATA_FRAMES
from Crypto.Cipher import AES
from io import BytesIO

import pandas as pd
import collections
import binascii
import datetime
import random
import string
import uuid
import json
import time
import os


"""FUNCTION DEFINITIONS"""
# Using 16bit zeroes as IV for the AES algo

IV = binascii.unhexlify('00000000000000000000000000000000')

def aes_128_cbc_encrypt(key, text):
    keyb = binascii.unhexlify(key)
    textb = binascii.unhexlify(text)
    encryptor = AES.new(keyb, AES.MODE_CBC, IV=IV)
    ciphertext = encryptor.encrypt(textb)
    return ciphertext.hex().upper()

def gen_ki():
    return str(uuid.uuid4()).replace('-', '').upper()

def gen_k4():
    return str(uuid.uuid4()).replace('-', '').upper() +str(uuid.uuid4()).replace('-', '').upper()

def gen_opc(op, ki):
    return (calc_opc_hex(ki, op).upper())


def xor_str(s, t):
  return bytes([_a ^ _b for _a, _b in zip(s, t)])

def calc_opc_hex(k_hex, op_hex):
  iv = binascii.unhexlify(16 * '00')
  ki = binascii.unhexlify(k_hex)
  op = binascii.unhexlify(op_hex)

  aes_crypt = AES.new(ki, mode=AES.MODE_CBC, IV=iv)
  data = op
  o_pc = xor_str(data, aes_crypt.encrypt(data))
  return o_pc.hex().upper()


def gen_eki(transport, ki):
    return aes_128_cbc_encrypt(transport, ki)


def gen_opc_eki(op, transport, ki):
    return {"opc": gen_opc(op, ki), "eki": gen_eki(transport, ki)}

def lenfunc(x):
  return len(x)

def gen_eki_custom(x):
  return gen_eki(k4,x)

def gen_opc_custom(x):
  return gen_opc(op,x)

def generate_8_Digit():
  return str(random.randint(10000000, 99999999))

def generate_4_Digit():
  return str(random.randint(1000, 9999))

def pin_func(x):
  return rpad(s2h(x), 16).upper()

def enc_imsi(imsi):
    imsi = str(imsi)
    l = half_round_up(len(imsi) + 1)  # Required bytes - include space for odd/even indicator
    oe = len(imsi) & 1			# Odd (1) / Even (0)
    ei = '%02x' % l + swap_nibbles('%01x%s' % ((oe << 3) | 1, rpad(imsi, 15)))
    return ei
def dec_imsi(ef):
    ef= str(ef)
    if len(ef) < 4:
        return None
    l = int(ef[0:2], 16) * 2		# Length of the IMSI string
    l = l - 1						# Encoded length byte includes oe nibble
    swapped = swap_nibbles(ef[2:]).rstrip('f')
    if len(swapped) < 1:
        return None
    oe = (int(swapped[0]) >> 3) & 1  # Odd (1) / Even (0)
    if not oe:
        l = l-1
    if l != len(swapped) - 1:
        return None
    imsi = swapped[1:]
    return imsi
Hexstr = str
def enc_iccid(iccid: str) -> Hexstr:
  iccid = str(iccid)
  luhn=calculate_luhn(iccid)
  iccid = iccid+str(luhn)
  m_iccid = swap_nibbles(rpad(iccid, 20))
  return m_iccid.upper()

def dec_iccid(ef: Hexstr) -> str:
  ef= str(ef)
  ef = ef.upper()
  iccid= swap_nibbles(ef).strip('F')
  return iccid[:-1]
def swap_nibbles(s: Hexstr) -> Hexstr:
    return ''.join([x+y for x, y in zip(s[1::2], s[0::2])])
def rpad(s: str, l: int, c='f') -> str:
    return s + c * (l - len(s))

def lpad(s: str, l: int, c='f') -> str:
    return c * (l - len(s)) + s

def half_round_up(n: int) -> int:
    return (n + 1)//2


def calculate_luhn(cc) -> int:
    num = list(map(int, str(cc)))
    check_digit = 10 - sum(num[-2::-2] + [sum(divmod(d * 2, 10))for d in num[::-2]]) % 10
    return 0 if check_digit == 10 else check_digit

def h2b(s: Hexstr) -> bytearray:
    return bytearray.fromhex(s)


def b2h(b: bytearray) -> Hexstr:
    return ''.join(['%02x' % (x) for x in b])


def h2i(s: Hexstr) -> List[int]:
    return [(int(x, 16) << 4)+int(y, 16) for x, y in zip(s[0::2], s[1::2])]


def i2h(s: List[int]) -> Hexstr:
    return ''.join(['%02x' % (x) for x in s])

def h2s(s: Hexstr) -> str:
  return ''.join([chr((int(x, 16) << 4)+int(y, 16)) for x, y in zip(s[0::2], s[1::2]) if int(x + y, 16) != 0xff])

def s2h(s: str) -> Hexstr:
  b = bytearray()
  b.extend(map(ord, s))
  return b2h(b)

def i2s(s: List[int]) -> str:
  return ''.join([chr(x) for x in s])

def integer_2_ascii(x):
  return s2h(x)

def apply_luhn_check(x):
  return str(x) + str(calculate_luhn(str(x)))

def copy_function(x):
  return str(x)

def PIN1_function(x):
    return str(params.get_PIN1())
def PUK1_function(x):
    return str(params.get_PUK1())
def PIN2_function(x):
    return str(params.get_PIN2())
def PUK2_function(x):
    return str(params.get_PUK2())
def ADM1_function(x):
    return str(params.get_ADM1())
def ADM6_function(x):
    return str(params.get_ADM6())
def ACC_function(x):
  return str(params.get_ACC())  
#  return str("0002")

def ACC_function1(x):
  return str(params.get_ACC())  
#  return str("0002")

#code below is for Demo Data generation, what if we have to gernate Data from ICCID and IMSI given
#we have to read input file and copy content [ICCID, IMSI] from input file and generate Parameters based on input File

def splitter(input_string):
  if (input_string != "" ) and (input_string.find("-")!= -1) and len(input_string)>2:
    values = input_string.split('-')
  else:
    values =[0,32]
  return int(values[0]),int(values[1])

def extract_values(t:list):
  R=[]
  L=[]
  for i in t:
    left,right =splitter(i)
    R.append((right))
    L.append((left))
  return L,R

def return_diplicates(x):
  return ([item for item, count in collections.Counter(x).items() if count > 1])

def get_dic_parameter(d:dict):
  va,cl,R,L = ([] for i in range(4))
  for i in range(len(d.keys())):
    va.append(list(d.values())[i][0])
    cl.append(list(d.values())[i][1])
    R1,L1=splitter(list(d.values())[i][2])
    R.append(R1)
    L.append(L1)
  va_renamed = append_count_to_duplicates(va)
  va_duplicate = return_diplicates(va)
  va_unique = set(va)
  return va_renamed,va_duplicate,va_unique,cl,R,L


def Generate_df_from_list(t_list:list,rows:int):
  df = pd.DataFrame()
  d1 = {}
  for i in range(len(t_list)):
    d1[str(t_list[i])] = 0
  new_data = [d1 for i in range(0, rows)]
  df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
  return df

def append_count_to_duplicates(input_list):
    output_list = []
    element_counts = {}

    for element in input_list:
        if element in element_counts:
            element_counts[element] += 1
            output_list.append(f"{element}{element_counts[element]}")
        else:
            element_counts[element] = 0
            output_list.append(element)

    return output_list




def Init_major(df,str1,init_v):
  for i in range(0,df.shape[0]):
    df.loc[i, str1] = str(init_v + i)


def Init_minor(df,str1,init_v):
  df[str1] = str(init_v)


def InitalizeDemoDataFrame(df,demo:bool,ICCID_start,IMSI_start):
  if demo is True:
    Init_major(df,"ICCID",ICCID_start) #major with incremetal pattern
    Init_major(df,"IMSI",IMSI_start)
  else:
    Init_minor(df,"ICCID",0) #major without incremetal pattern
    Init_minor(df,"IMSI",0)

  Init_minor(df,"PIN1",0)
  Init_minor(df,"PUK1",0)
  Init_minor(df,"PIN2",0)
  Init_minor(df,"PUK2",0)
  Init_minor(df,"KI",0)
  Init_minor(df,"EKI",0)
  Init_minor(df,"ADM1",0)
  Init_minor(df,"ADM6",0)
  Init_minor(df,"OPC",0)
  Init_minor(df,"ACC",0)
#  df['len_KI'] = 0
#  df['len_EKI'] = 0
#  df['len_OPC'] = 0
  return df

def apply_function(df,dest:str,src:str,function):
  if dest in df.columns: df[dest] = df[src].apply(function).copy(deep=False)


def Apply_functions(df,op_1,k4_1):
#  print(k4_1,op_1)
  apply_function(df,'ICCID','ICCID',apply_luhn_check)
  apply_function(df,'IMSI','IMSI',copy_function)

  if params.get_PIN1_RAND() is False:
    apply_function(df,'PIN1','PIN1',lambda x: generate_4_Digit()) #Reason: PIN1 is fixed for now  
  else:
    apply_function(df,'PIN1','PIN1',PIN1_function) #Reason: PIN1 is fixed for now

  if params.get_PUK1_RAND() is False:
    apply_function(df,'PUK1','PUK1',lambda x: generate_8_Digit())
  else:
    apply_function(df,'PUK1','PUK1',PUK1_function)

  if params.get_PIN2_RAND() is False:
    apply_function(df,'PIN2','PIN2',lambda x: generate_4_Digit())
  else:
    apply_function(df,'PIN2','PIN2',PIN2_function)

  if params.get_PUK2_RAND() is False:
    apply_function(df,'PUK2','PUK2',lambda x: generate_8_Digit())
  else:
    apply_function(df,'PUK2','PUK2',PUK2_function)

  if params.get_ADM1_RAND() is False:
    apply_function(df,'ADM1','ADM1',lambda x: generate_8_Digit())
  else:
    apply_function(df,'ADM1','ADM1',ADM1_function)

  if params.get_ADM6_RAND() is False:
    apply_function(df,'ADM6','ADM6',lambda x: generate_8_Digit())
  else:
    apply_function(df,'ADM6','ADM6',ADM6_function)

  apply_function(df,'KI','KI',lambda x: gen_ki())
  apply_function(df,'EKI','KI',gen_eki_custom)
  apply_function(df,'OPC','EKI',gen_opc_custom)

  if params.get_ACC_RAND():
    apply_function(df,'ACC','ACC',lambda x: generate_4_Digit())
  else:
    apply_function(df,'ACC','ACC',ACC_function)
  return df

def drop_extra_columns(list_pass:list, dataframe):
  columns_to_drop = [col for col in dataframe.columns if col not in list_pass]
  data = dataframe.drop(columns=columns_to_drop).copy(deep=False)
  return data

def Clip_columns(df,l:list,r:list):
  count= 0
  dict2={}
  for col in df.columns:
    dict2[col]=count
    count+=1
  for col in df.columns:    
    df[col] = df[col].apply(lambda x: x[l[dict2[col]]:r[dict2[col]]+1]).copy(deep=False)
  return df

  
def add_duplicate_var(df,limit:int,h1:list):
  for c in range(limit):
    for col in default_headers:
      if col+str(c) in h1: df[col+str(c)] = df[col].copy(deep=False)
  return df[h1] #df[h] reason: to return index of df according to header

def Encoding(df):
  if 'ICCID' in df.columns: df["ICCID"] = df["ICCID"].apply(enc_iccid).copy(deep=False)
  if 'IMSI' in df.columns: df["IMSI"] = df["IMSI"].apply(enc_imsi).copy(deep=False)
  if 'PIN1' in df.columns: df["PIN1"] = df["PIN1"].apply(pin_func).copy(deep=False)
  if 'PUK1' in df.columns: df["PUK1"] = df["PUK1"].apply(integer_2_ascii).copy(deep=False)
  if 'PIN2' in df.columns: df["PIN2"] = df["PIN2"].apply(pin_func).copy(deep=False)
  if 'PUK2' in df.columns: df["PUK2"] = df["PUK2"].apply(integer_2_ascii).copy(deep=False)
  if 'ADM1' in df.columns: df["ADM1"] = df["ADM1"].apply(integer_2_ascii).copy(deep=False)
  return df




def non_demo(default_headers1,op_3,k4_3): 
  data=dataframes.INPUT_DF
  df1 = Generate_df_from_list(default_headers1,data.shape[0])
  #df3 = InitalizeDemoDataFrame(df2,demo=demo_Data)
#  print([(c, data[c].dtype.kind in 'iufcb') for c in data.columns])

  df1['ICCID']= data['ICCID']
  df1['IMSI']= data['IMSI']
  non_demo_data = Apply_functions(df1,op_3,k4_3)
  return non_demo_data

def is_demo(default_headers1,op_3:str,k4_3:str):
#  empty_df = Generate_df_from_list(default_headers1,int(size))
  empty_df = Generate_df_from_list(default_headers1,int(params.get_DATA_SIZE()))
  demo_data_init = InitalizeDemoDataFrame(empty_df,demo=True,ICCID_start=int(params.get_ICCID()),IMSI_start=int(params.get_IMSI()))
  demo_data = Apply_functions(demo_data_init,op_3,k4_3)
  return demo_data

def _DATA_PARSER_INITIAL(demo_data1:bool,default_headers2:list,op_4,k4_4,keys:bool):
  if keys:
    dict_keys={"k4":k4_4,"op":op_4}
  else:
    dict_keys={"k4":"","op":""}
  if demo_data1 is True:
    return is_demo(default_headers2,op_4,k4_4),dict_keys
  
  if demo_data1 is False:
    return non_demo(default_headers2,op_4,k4_4),dict_keys

def _DATA_PARSER_FINAL(input_dict:dict,df_input,clip:bool,encoding:bool,caption:str):
  laser_h,laser_d_h,laser_unique,laser_c,laser_l,laser_r =get_dic_parameter(input_dict)
  df20 = df_input.copy(deep=False)
  if encoding is True: 
    emcoded_df = Encoding(df20)
  else: 
    emcoded_df = df20.copy(deep=False)
#  print(laser_l)
#  print(laser_r)

  dupl_var_encoded_df = add_duplicate_var(emcoded_df,10,laser_h)
  dupl_var_encoded_df = dupl_var_encoded_df.copy(deep=False)
  #df23 = drop_extra_columns(laser_h,df7)
  #df24 = df22.copy(deep=False)
  if clip is True: 
    final_df = Clip_columns(dupl_var_encoded_df,laser_l,laser_r)
  else:
    final_df = dupl_var_encoded_df.copy(deep=False) 
#  final_df.style.set_caption("|=="+caption+"==|")
  return final_df


input_elect_params= {
    '0': ['ICCID', 'Normal', "0-10"],
    '1': ['ICCID', 'Normal', "0-32"],
    '2': ['PIN1', 'Normal', "0-32"],
    '3': ['PUK1', 'Normal', "0-32"],
    '4': ['PUK1', 'Normal', "0-32"],
    '5': ['PIN2', 'Normal', "0-32"],
    '6': ['PUK2', 'Normal', "0-32"],
    '7': ['ADM1', 'Normal', "0-32"],
    '8': ['ADM6', 'Normal', "0-32"],
    '9': ['KI', 'Normal', "0-32"],
    '10': ['EKI', 'Normal', "0-32"],
    '11': ['OPC', 'Normal', "0-32"],
    '12': ['ACC', 'Normal', "0-3"]
    }
input_laser_params= {
    '0': ['ICCID', 'Right', "0-31"],
    '1': ['IMSI', 'Right', "0-31"]
  }

#del df['len_KI']
#del df['len_EKI']
#del df['len_OPC']

"""LASER DATA"""

# temp = encoded_data["KI"]
# temp.to_csv("keys.txt",index= False)
# f = open('keys.txt', 'a')
# f.write('OP : '+op)
# f.write('Transport key : '+k4)
# f.close()




#parameters to get from App Python QT
data_size = 10*1
demo_Data= True
IMSI_start = 999990000000400
ICCID_start = 999900000000000400
PIN1="0000"
PUK1="11223344"
PIN2="1234"
PUK2="12345678"
ADM1="12345678"
ADM6="12345678"
ACC="0001"
op = "1111006F86FAD6540D86FEF24D261111"  # zong
k4 = "111150987DE41E9F0808193003B543296D0A01D797B511AFDAEEEAC53BC61111" #zong

params=PARAMETERS()
dataframes=DATA_FRAMES()
#===========================================#  
#===================SET=====================#  
#===========================================#  

def SET_ALL():
  params.set_K4(k4)
  params.set_OP(op)
  params.set_IMSI(IMSI_start)        
  params.set_ICCID(ICCID_start)
  params.set_PIN1(PIN1)
  params.set_PUK1(PUK1)
  params.set_PIN2(PIN2)
  params.set_PUK2(PUK2)
  params.set_ADM1(ADM1) 
  params.set_ADM6(ADM6)
  params.set_ACC(ACC)
  params.set_DATA_SIZE(data_size)

  params.set_DEMO_CHECK(False)
  params.set_ELECT_CHECK(True)
  params.set_GRAPH_CHECK(True)
  params.set_ELECT_DICT(input_elect_params)
  params.set_GRAPH_DICT(input_laser_params)
  params.set_INPUT_PATH("C:/Users/hamza.qureshi/Desktop/STC_APP/improvements/dataGen-v17/input.csv")
#========================================#  
#========================================#  
#========================================#  

  params.set_PIN1_RAND(False)
  params.set_PUK1_RAND(True)
  params.set_PIN2_RAND(False)
  params.set_PUK2_RAND(False)
  params.set_ADM1_RAND(False)
  params.set_ADM6_RAND(True)
  params.set_ACC_RAND(False)

#===========================================#  
#==================GET======================#  
#===========================================#  


# parameter_dict={
#   "Demo Data":"","OP":"","K4":"","ICCID":"","IMSI":"",
#   "PIN1":"","PUK1":"","PIN2":"","PUK2":"","ADM1":"",
#   "ADM6":"","ACC":"","DATA_SIZE":""}
def GET_ALL_PARAMS_DICT()->dict:
    param_dict={}
    param_dict["Demo Data"]=params.get_DEMO_CHECK()
    param_dict["OP"]=params.get_OP()
    param_dict["K4"]=params.get_K4()
    param_dict["ICCID"]=params.get_ICCID()
    param_dict["IMSI"]=params.get_IMSI()
    param_dict["PIN1"]=params.get_PIN1()
    param_dict["PUK1"]=params.get_PUK1()
    param_dict["PIN2"]=params.get_PIN2()
    param_dict["PUK2"]=params.get_PUK2()
    param_dict["ADM1"]=params.get_ADM1()
    param_dict["ADM6"]=params.get_ADM6()
    param_dict["ACC"]=params.get_ACC()
    param_dict["DATA_SIZE"]=params.get_DATA_SIZE()
    param_dict["INPUT_PATH"]=params.get_INPUT_PATH()
    return param_dict


input_file_path = 'input.csv'

default_headers = ['ICCID','IMSI','PIN1','PUK1','PIN2','PUK2','KI','EKI','OPC','ADM1','ADM6','ACC']



#==============================================================#
#========================LASER DATA============================#
#==============================================================#


input_elect_params= {
    '0': ['ICCID', 'Normal', "0-19"],
    '1': ['IMSI', 'Normal', "0-14"],
    '2': ['PIN1', 'Normal', "0-3"],
    '3': ['PUK1', 'Normal', "0-7"],
    '5': ['PIN2', 'Normal', "0-3"],
    '6': ['PUK2', 'Normal', "0-7"],
    '7': ['ADM1', 'Normal', "0-7"],
    '8': ['ADM6', 'Normal', "0-7"],
    '10': ['EKI', 'Normal', "0-31"],
    '11': ['OPC', 'Normal', "0-31"],
    '12': ['ACC', 'Normal', "0-3"]
    }

#==============================================================#
#=====================ELECTRICAL DATA==========================#
#==============================================================#



# def preview_files_new1(graphical:bool,electrical:bool,laser_dict:dict,elect_dict:dict):
#   Initial_DataFrame = pd.DataFrame()
#   Initial_DataFrame,keys_dict = _DATA_PARSER_INITIAL(demo_data1=True,
#                                            default_headers2=default_headers,
#                                            data_size2=data_size,
#                                            ICCID3=ICCID_start,
#                                            IMSI3=IMSI_start,
#                                            input_file_path3=input_file_path,
#                                            op_4=op,
#                                            k4_4=k4,
#                                            keys=True)
#   laser_df=pd.DataFrame()
#   elect_df=pd.DataFrame()

#   if graphical is True:
#     laser_df=_DATA_PARSER_FINAL(laser_dict,Initial_DataFrame,clip=True,encoding=False,caption='LASER')
#   if electrical is True:
#     elect_df=_DATA_PARSER_FINAL(elect_dict,Initial_DataFrame,clip=False,encoding=True,caption='ELECT')
#   return elect_df,laser_df,keys_dict

def preview_files_gets():
  Initial_DataFrame = pd.DataFrame()
  Initial_DataFrame,keys_dict = _DATA_PARSER_INITIAL(demo_data1=params.get_DEMO_CHECK(),
                                           default_headers2=default_headers,
                                           op_4=params.get_OP(),
                                           k4_4=params.get_K4(),
                                           keys=True)
#  print(Initial_DataFrame)
  
  laser_df=pd.DataFrame()
  elect_df=pd.DataFrame()

  if params.get_GRAPH_CHECK() is True:
    laser_df=_DATA_PARSER_FINAL(params.get_GRAPH_DICT(),Initial_DataFrame,clip=True,encoding=False,caption='LASER')
  if params.get_ELECT_CHECK() is True:
    elect_df=_DATA_PARSER_FINAL(params.get_ELECT_DICT(),Initial_DataFrame,clip=False,encoding=True,caption='ELECT')
  
  return elect_df,laser_df,keys_dict


#print(dataframes.INPUT_DF)
# print("DEBUG")
# SET_ALL()
# dataframes.INPUT_DF=pd.read_csv(params.get_INPUT_PATH())
# print(dataframes.INPUT_DF.info())
# parameter_dict=GET_ALL_PARAMS_DICT()
# print(parameter_dict)
# elect,laser,keys= preview_files_gets()
# #print(elect)
# print(laser.to_string())
# #print(parameter_dict)


