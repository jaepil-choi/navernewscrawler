import multiprocessing as mp

import argparse
from pathlib import Path
import pickle
# import jsonpickle

## Import custom libs
from navernewscrawler import worker



def check_pickle(filename):
    cwd = Path('.').resolve()

    assert (cwd / filename).exists()



if __name__ == '__main__':
    check_pickle('sid_list.pickle')
    check_pickle('kospi_ii2dates.pickle')
    check_pickle('kosdaq_ii2dates.pickle')
    check_pickle('kospi_ii2codename_combined')
    check_pickle('kosdaq_ii2codename_combined')

    with open('sid_list.pickle', 'rb') as f:
        sid_list = pickle.load(f)
    with open('kospi_ii2dates.pickle', 'rb') as f:
        kospi_ii2dates = pickle.load(f)
    with open('kosdaq_ii2dates.pickle', 'rb') as f:
        kosdaq_ii2dates = pickle.load(f)
    with open('kospi_ii2codename_combined.pickle', 'rb') as f:
        kospi_ii2codename = pickle.load(f)
    with open('kosdaq_ii2codename_combined.pickle', 'rb') as f:
        kosdaq_ii2codename = pickle.load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--processes', '-p', type=int, help='Number of processes for multiprocessing')
    args = parser.parse_args()

    num_processes = args.processes

    with mp.Pool(processes=num_processes) as p:
        mp_result = p.map(worker.generate_ii_newsdata, sid_list)

    
