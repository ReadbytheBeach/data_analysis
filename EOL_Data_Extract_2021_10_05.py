# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import numpy as np
import pandas as pd
import os

# get file path and file name
path1 = os.getcwd() + '\\Data\\'  # Put all test data in 'Data' folder, path is in one level down of script
path2 = os.getcwd() + '\\Data\\EOL_Data_Extract_Result\\'  # store output file in path 2
print(path1)
file_list = os.listdir(path1)
cvs_list = []

# only choose csv data file for further processing, delete folder item in the list
for i in file_list:
    if i[len(i)-4:] == '.csv':
            cvs_list.append(i)

print('Batch File List: ')
print(cvs_list)
print('------------------------------')

# batch processing all data
for file_index in cvs_list:
    f = pd.read_csv(path1 + file_index, header=None, names=['ID',	'Distance',	'Speed', 'Angle', 'Mag', 'Kstate', 'vehicleSpeed', 'X_Lateral',
                          'Y_Longtitudinal', 'X_Speed', 'Y_Speed', 'radius', 'timeInterval', 'Target[i].isuse',
                         'cntCaniTrk', 'noise', 'yaw_rate', 'almType'])
    df = pd.DataFrame(f)

# select EOL result rows
    temp = df.loc[df['ID'] == 'END']
    temp_array = np.array(temp)
    eol_df = pd.DataFrame(temp_array, columns=['Name', 'NoofRawTarget', 'Angle', 'eolCnt', 'eolAngle', 'tx_s_cnt_Tx1',
                                               'tx_s_cnt_Tx2', 'txstd_Tx1', 'txstd_Tx2', 'tx_probability_Tx1',
                                               'tx_probability_Tx2', 'txcnt_Tx1', 'txcnt_Tx2', 'txavg_Tx1', 'txavg_Tx2', 'Times', 'NA', 'NA'])
    eol_df = eol_df.iloc[:, 1:16]   # delete column 'Name' and 'NA'

    for i in eol_df.head(0):
        if type(eol_df.at[0, i]) == str:
                temp_df = eol_df[i].str.split(':', expand=True)  # split str content to 2 column: Str [0] and Number [1]
                eol_df[i] = temp_df[1]

    file_output = file_index[0:len(file_index)-4] + '_eol_extract.csv'
    eol_df.to_csv(path2 + file_output, index=False, header=True)
    print(file_index + ': finished')

# print(eolresult_df)
# for i in range(0,200)
#    if 'END' in df.iloc[i]:
#        temp.append=df.iloc[3,0:5]
# get size of df
# df_shape = eol_df.shape
# x=d_shape[0] #get number of rows
# y=df_shape[1] #get number of columns
# bool = eol_df['Angle'].str.contains(':') #check if column 'Angle' contains ':'
# print(type(eol_df.at[0,'Angle']))
# print(type(eol_df.at[0,'tx_s_cnt_Tx2']))
#  temp = pd.concat([temp,temp2],axis=1)
#  temp = pd.merge(temp,temp2,how='outer')