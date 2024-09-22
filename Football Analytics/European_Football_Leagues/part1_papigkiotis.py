import pandas as pd
import glob
import os

folder_path1 = r'C:\Users\User\Desktop\Python\Kaizen Project\Junior_Quant_-_Case_Study_-_Data\Data\Part1\ENG'
folder_path2 = r'C:\Users\User\Desktop\Python\Kaizen Project\Junior_Quant_-_Case_Study_-_Data\Data\Part1\FRA'
folder_path3 = r'C:\Users\User\Desktop\Python\Kaizen Project\Junior_Quant_-_Case_Study_-_Data\Data\Part1\SPA'


premier_league_files = glob.glob(os.path.join(folder_path1, '*.csv'))
league_1_files = glob.glob(os.path.join(folder_path2, '*.csv'))
la_liga_files = glob.glob(os.path.join(folder_path3, '*.csv'))


premier_league_data_list = [pd.read_csv(file) for file in premier_league_files]
league_1_data_list = [pd.read_csv(file) for file in league_1_files]
la_liga_data_list = [pd.read_csv(file) for file in la_liga_files]


premier_league_df = pd.concat(premier_league_data_list, ignore_index = True)
league_1_df = pd.concat(league_1_data_list, ignore_index = True)
la_liga_df = pd.concat(la_liga_data_list, ignore_index = True)

premier_league_df.to_csv(r'C:\Users\User\Desktop\Python\Kaizen Project\Junior_Quant_-_Case_Study_-_Data\Data\Part1\combined_output.csv', index=False)
league_1_df.to_csv(r'C:\Users\User\Desktop\Python\Kaizen Project\Junior_Quant_-_Case_Study_-_Data\Data\Part1\combined_output1.csv', index=False)
la_liga_df.to_csv(r'C:\Users\User\Desktop\Python\Kaizen Project\Junior_Quant_-_Case_Study_-_Data\Data\Part1\combined_output2.csv', index=False)





