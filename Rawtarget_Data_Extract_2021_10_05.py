# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Author is Wu Jun

import numpy as np
import pandas as pd
import os

# get file path and file name
path1 = os.getcwd() + '\\Data\\'  # Put all test data in 'Data' folder, path is in one level down of script
path2 = os.getcwd() + '\\Data\\Rawtarget_Data_Extract_Result\\'  # store output file in path 2
print('Original files are in ' + path1)
file_list = os.listdir(path1)
cvs_list = []

# only choose csv data file for further processing, delete folder item in the list

for i in file_list:
    if i[len(i)-4:] == '.csv':
            cvs_list.append(i)

print('Batch File List: ' + str(cvs_list))
print('-------------------------------------------------------------------------------------------------------------')

# batch processing all data
for file_index in cvs_list:
    f = pd.read_csv(path1 + file_index, header=None, names=['ID',	'Distance',	'Speed', 'Angle', 'Mag', 'Kstate', 'vehicleSpeed', 'X_Lateral',
                          'Y_Longtitudinal', 'X_Speed', 'Y_Speed', 'radius', 'timeInterval', 'Target[i].isuse',
                         'cntCaniTrk', 'noise', 'yaw_rate', 'almType'])
    df = pd.DataFrame(f)
    df_shape = df.shape
#    print(df_shape)
#    df_shape[0]  # get number of rows
#    df_shape[1]  # get number of columns
# 'START' value refers new frame of data
    index_frame = df.loc[df['ID'] == 'START'].index.tolist()
# '1024' means demarcation point in 'Distance' column, Tx1 raw target list is above and Tx2 raw target is below it
    index_Txmodule = df.loc[df['Distance'] == '1024'].index.tolist()
    n_frame = len(index_frame)  # Get number of frames
# Creating variable (list, int...) for storing wanted value
    frameNb = []
    Tx_module = []
    ID_rawtarget = []
    R_rawtarget = []
    V_rawtarget = []
    A_rawtarget = []
    Mag_rawtarget = []
    i = 0
    # staring to get value of each record
    for i in range(0, n_frame):
        if i <= n_frame - 2:  # last frame end index is not included in index_frame, df index is used.
            n_rawtarget = index_frame[i+1] - index_frame[i] - 4  # there are 3 lines heander and 1 lines trailer in per frame data
            # Getting ID column value
            temp_list = df['ID'].values.tolist()
            ID_rawtarget.extend(temp_list[index_frame[i]+3 : int(index_frame[i])+n_rawtarget+3])
            # Getting Distance value
            temp_list = df['Distance'].values.tolist()
            R_rawtarget.extend(temp_list[index_frame[i]+3 : int(index_frame[i])+n_rawtarget+3])
            # Getting Speed value
            temp_list = df['Speed'].values.tolist()
            V_rawtarget.extend(temp_list[index_frame[i]+3 : int(index_frame[i])+n_rawtarget+3])
            # Getting Angle value
            temp_list = df['Angle'].values.tolist()
            A_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            # Getting Mag value
            temp_list = df['Mag'].values.tolist()
            Mag_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            # creating frameNb value and Tx module value
            for j in range(0, n_rawtarget):
                frameNb.append(i)
                if j < int(df.at[index_Txmodule[i], 'ID']):
                    Tx_module.append('Tx1')
                elif j == int(df.at[index_Txmodule[i], 'ID']):  #if the ID of raw target is '1024', then the row is no meaning value
                    Tx_module.append('NA')
                else:
                    Tx_module.append('Tx2')
        else:
            n_rawtarget = df_shape[0] - index_frame[i] - 4
            temp_list = df['ID'].values.tolist()
            ID_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            temp_list = df['Distance'].values.tolist()
            R_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            temp_list = df['Speed'].values.tolist()
            V_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            temp_list = df['Angle'].values.tolist()
            A_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            temp_list = df['Mag'].values.tolist()
            Mag_rawtarget.extend(temp_list[index_frame[i] + 3: int(index_frame[i]) + n_rawtarget + 3])
            for j in range(0, n_rawtarget):
                frameNb.append(i)
                if j < int(df.at[index_Txmodule[i], 'ID']):
                    Tx_module.append('Tx1')
                elif j == int(df.at[index_Txmodule[i], 'ID']):
                    Tx_module.append('NA')
                else:
                    Tx_module.append('Tx2')
    # combining all list in to dataframe, via Dict class
    rawtarget_df = pd.DataFrame({'frameNb' : frameNb, 'Tx_Module': Tx_module, 'ID': ID_rawtarget, 'Distance': R_rawtarget,
                                 'Angle': A_rawtarget, 'Speed': V_rawtarget, 'Mag':Mag_rawtarget})
    file_output = file_index[0:len(file_index) - 4] + '_extract.csv'
    rawtarget_df.to_csv(path2 + file_output, index=False, header=True)
    print(file_index + ': finished')
    print('Dataframe size is ' + str(rawtarget_df.shape))
#       frameNb.append(frameNb_temp)
print('-------------------------------------------------------------------------------------------------------------')
print('total ' + str(len(cvs_list)) + ' files are processed') # summary
print('All processed data are stored in ' + path2)

#  temp = pd.concat([temp,temp2],axis=1)
#  temp = pd.merge(temp,temp2,how='outer')