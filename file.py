
import re
import pandas as pd



def read_vars(file)->dict:
    pattern = r'(\w+)\s*:\s*(.+)'
    flags = re.UNICODE
    matches = re.findall(pattern, file, flags=flags)
    dict1={}
    for match in matches:
        variable = match[0]
        value = match[1]
        dict1[variable]=value
    print("========================VARIABLES============================")
#    print(dict1)
    return dict1

# def read_df(file):  
#     print(file)   
#     df_start = file.find("DATAFRAME_START")
#     df_end = file.find("DATAFRAME_END")
#     df_content = file[df_start+len("DATAFRAME_START"):df_end]

#     print("========================DATAFRAME============================")
# #    print(df_content)
#     return df_content
def read_df(file):  
    df_content=pd.DataFrame(file)
    print(df_content)
    return df_content

# with open('input1.csv', 'r', encoding='utf-8') as file:
#    fp = file.read()
# read_vars(fp)

def count_invalid_lines():
    with open('input1.csv', 'r', encoding='utf-8') as file:
        fp = file.read()
    count=0
    for line in fp:
        if line == "DATAFRAME_START":
            count=+1
    print(count)
    return count
#count_invalid_lines()
#df=pd.read_csv('input1.csv',skiprows=count_invalid_lines())
#print(df)
#read_df(fp)


import re
import pandas as pd

# # Open the file
# with open('input1.csv', 'r', encoding='utf-8') as file:
#    fp = file.read()

# Extract variables using regular expressions
# variable_pattern = r'(\w+)\s*:\s*(.+)'
# flags = re.UNICODE
#matches = re.findall(pattern, file, flags=flags)

#variable_matches = re.findall(variable_pattern, contents,flags=flags)
#variables = dict(variable_matches)
#===============
def get_var_df(contents):
    pattern = r'(\w+)\s*:\s*(.+)'
    flags = re.UNICODE
    matches = re.findall(pattern, contents, flags=flags)
    dict1={}
    for match in matches:
        variable = match[0]
        value = match[1]
        dict1[variable]=value

# Extract DataFrame content
    df_start = contents.find('var_out:')
    df_content = contents[df_start + len('var_out:'):]

# Create DataFrame from the content
    data = [line.split() for line in df_content.split('\n') if line.strip()]
    column_names = data[0]
    df_data = data[1:]
    df = pd.DataFrame(df_data, columns=column_names)
    return df,dict1

# df,dict1=get_var_df(fp)

# # Print the variables and DataFrame
# #=========================================================#
# #=========================================================#
# #=========================================================#
# #=========================================================#

# print("Variables:")
# for key, value in dict1.items():
#     print(f"{key}: {value}")

# print("\nDataFrame:")
# print(df)
# #s = pd.Series(dict1, name='DateValue')
# #print(s)