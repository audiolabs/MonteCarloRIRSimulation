import os
import argparse
import importlib
from config.config import * 

if __name__ == '__main__':
    os.makedirs('./'+data_path, exist_ok=True)
    Number_of_Rooms = len(rooms)
    for r in range(Number_of_Rooms):
        for s_a_dist in source_array_dist:
            for revTime in reverberationtimes:
                for i in range(reps):
                    print(str(rooms[r][0]),str(rooms[r][1]),str(rooms[r][2]), str(s_a_dist), str(revTime),str(dmic), data_path,array_type,str(num_mics),str(i), doa_count)
