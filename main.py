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

check_pickle('sid_list.pickle')
check_pickle('kospi_ii2dates.pickle')
check_pickle('kosdaq_ii2dates.pickle')
check_pickle('kospi_ii2codename_combined.pickle')
check_pickle('kosdaq_ii2codename_combined.pickle')

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

def wrap_worker(
    sid, 
    kospi_ii2dates=kospi_ii2dates,
    kosdaq_ii2dates=kosdaq_ii2dates,
    kospi_ii2codename=kospi_ii2codename,
    kosdaq_ii2codename=kosdaq_ii2codename,
    ):

    return worker.generate_ii_newsdata(
        sid,
        kospi_ii2dates,
        kosdaq_ii2dates,
        kospi_ii2codename,
        kosdaq_ii2codename,
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--processes', '-p', type=int, help='Number of processes for multiprocessing')
    args = parser.parse_args()

    num_processes = args.processes

    if num_processes:
        print(f'Start multiprocessing with {num_processes} processes')
        with mp.Pool(processes=num_processes) as p:
            mp_result = p.map(wrap_worker, sid_list)
    else:
        print('Start without multiprocessing ')
        result = []
        for sid in sid_list:
            wrap_worker(sid)
            result.append(sid)

    
