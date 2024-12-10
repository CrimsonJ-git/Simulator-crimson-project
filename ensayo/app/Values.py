from Process import get_data, source_data

data_1 = get_data('vo_1', 'vr1', 'l1')
data_2 = get_data('vo_2', 'vr2', 'l2')
data_3 = get_data('vo_3', 'vr3', 'l3')
data_4 = get_data('vo_4', 'vr4', 'l4')
data_s = source_data()

import subprocess

subprocess.run(['python','Exe.py'])