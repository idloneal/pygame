import os


level_0 = {}

path_file = '../levels/0/'
name_file = os.listdir(path_file)
for temp in name_file:
     name = temp[8:-4]
     level_0[name] = path_file + temp
