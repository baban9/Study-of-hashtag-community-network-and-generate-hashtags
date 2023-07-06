import pandas as pd 
import config
import ast 
from collections import Counter 

hashtag_meta_data_file = config.HASHTAG_META_DATA
output_file_name = config.OUTPUT_FILE_LOC

df = pd.read_csv(hashtag_meta_data_file)
temp_ = []
for val in df['hash_combo'].to_list():
    res = ast.literal_eval(val)
    temp_.extend(res)

hash_combo_counts = Counter(temp_)
results = []
for ix, row in df.iterrows():
    f_name = row['file_name']
    like_ = row['like']
    res = ast.literal_eval(row['hash_combo'])
    for combo in res:
        c_value = hash_combo_counts[combo]
        results.append([f_name, like_, c_value, combo[0], combo[1]])

df = pd.DataFrame(results, columns=['f_name', "likes", "count", 'left', 'right'])
df.to_csv(output_file_name, index=False)