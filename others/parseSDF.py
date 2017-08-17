import os
import re
import pandas as pd
"""
write this script for LTZ to parse a SDF format file to CSV format
Belter, 20170817
"""

data_dir = r'..\data'
file = r'LMSDFDownload6Dec16FinalST.sdf'

all_fields = ['recode_id', 'PUBCHEM_SUBSTANCE_URL', 'LIPID_MAPS_CMPD_URL', 'LM_ID',
              'COMMON_NAME', 'CATEGORY', 'MAIN_CLASS', 'SUB_CLASS', 'CHEBI_ID',
              'INCHI_KEY', 'INCHI', 'STATUS', 'SYSTEMATIC_NAME',
              'SYNONYMS', 'EXACT_MASS', 'FORMULA', 'LIPIDBANK_ID',
              'PUBCHEM_SID', 'PUBCHEM_CID', 'KEGG_ID', 'HMDBID']
with open(os.path.join(data_dir, file), 'r') as f_handle:
    a_line = ''
    total_recodes = []
    for i in f_handle:
        i = i.strip()
        if i != '$$$$':
            a_line += i + '@'
        else:
            total_recodes.append(a_line)
            a_line = ''
    a_df = pd.DataFrame(columns=all_fields)  # Pandas DataFrame simplified this code
    for l in total_recodes:
        line_value = []
        for key in all_fields:
            value = ''
            if key == 'recode_id':
                value = re.search(r'^(LMST\d+)', l).group(1)
            else:
                try:  # 可以在正则表达式中插入变量
                    value = re.search(r'{}>@(.*?)@'.format(key), l).group(1)
                except:
                    print(key)
            line_value.append(value)
        a_df.loc[len(a_df)] = line_value
    a_df.to_csv(os.path.join(data_dir, 'result2.csv'), sep=',', index=False, header=True)

