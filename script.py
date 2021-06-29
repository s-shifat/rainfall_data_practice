import pandas as pd
import numpy as np
import os
from sys import exit

# constants
RAINFALL_FILE = input('Rainfall File Name>> ') or './rainfall_2008.csv'
LAT_FILE = input('Lat File Name>> ') or './lat.csv'
LON_FILE = input('Lon File Name>> ') or  './lon.csv'
QUERY_FILE = './query.xlsx'

class RainExtractor:
    def __init__(self) -> None:
        self.rainfall_data = pd.read_csv(RAINFALL_FILE, header=None, skip_blank_lines=True)
        self.lat = np.fromfile(LAT_FILE, sep=',') # row
        self.lon = np.fromfile(LON_FILE, sep=',') # col
        # setting lon values as rain data frame's column
        self.rainfall_data.columns = self.lon 
        # Now preparing column for longitudinal data
        data_perday = len(self.lat)
        number_of_days = len(self.rainfall_data)//data_perday
        ones_matrix = np.ones((number_of_days, data_perday)) # an 2D array of ones to broadcast the lat values to equal times of rainfall data length, this is done to avoid loop.
        self.lat_column = (ones_matrix * self.lat).flatten() # converting 2D array to 1D array
        self.rainfall_data['lat'] = self.lat_column
        print(self.rainfall_data.head(), self.rainfall_data.shape, sep='\n')
        self.result_file_name = ''
        self.outdf = pd.DataFrame()
    
    def query(self, lat_x, lon_y,save=False, interface=False):
        result = self.rainfall_data.loc[self.rainfall_data['lat']==lat_x, lon_y]
        if save:
            self.result_file_name = f"lat_{lat_x}-lon_{lon_y}"
            result.to_csv(self.result_file_name+'.csv',index=False, na_rep='NaN', header=False,sep=',')
        self.outdf[self.result_file_name] = result
        print('Results:',self.outdf, sep='\n')
        if interface:
            self.interface()

    def query_file(self, file_name):
        df = pd.read_excel(file_name, index_col=None)
        output_folder_path = os.path.join('.',RAINFALL_FILE.replace('.csv','')+'_results')
        try:
            os.mkdir(output_folder_path)
        except FileExistsError:
            pass
        os.chdir(output_folder_path)
        for _, data_series in df.iterrows():
            self.query(data_series.lat, data_series.lon, save=True)
        self.outdf.to_csv('results_combined.csv', index=False, na_rep='NaN',sep=',')
        os.chdir('../')

    def interface(self):
        choice = input('1. single query\n2. file query\n3. exit\n>> ')
        if choice == '1':
            lat = float(input('lat>> '))
            lon = float(input('lon>> '))
            self.query(lat, lon, save=True, interface=True)
        if choice == '2':
            file_name = input('Query File Name>> ') or QUERY_FILE
            self.query_file(file_name)
        else:
            exit()
        print('-'*10)
        self.interface()
            
if __name__ == '__main__':
    rain = RainExtractor()
    rain.interface()