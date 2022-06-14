import multiprocessing as mp

import argparse
from pathlib import Path
import pickle
import json

import logging
import traceback
import time
from datetime import timedelta, datetime
# import jsonpickle

from tqdm import tqdm

## Import custom libs
from navernewscrawler import worker, utils

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

    try:
        res = worker.generate_ii_newsdata(
            sid,
            kospi_ii2dates,
            kosdaq_ii2dates,
            kospi_ii2codename,
            kosdaq_ii2codename,
            )

        return res

    except Exception as e:
        print(traceback.format_exc())
        print(repr(e))
        print(f'** WARNING ** {sid} raised Exception. Skipping this company. Check the log.')

        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--processes', '-p', type=int, help='Number of processes for multiprocessing')
    parser.add_argument('--test', '-t', action='store_true')
    args = parser.parse_args()

    is_test = args.test
    num_processes = args.processes

    if is_test:
        with open('sid_list_test.json', 'r') as j:
            sid_list = json.load(j)['data']

    start_time = time.time()
    print(f'{utils.timestamp2formatted(start_time)} : Job started')
    if num_processes:
        print(f'Start multiprocessing with {num_processes} processes')
        with mp.Pool(processes=num_processes) as p:
            # mp_result = tqdm(p.imap(wrap_worker, sid_list), total=len(sid_list))
            mp_result = p.map(wrap_worker, sid_list)
    else:
        print('Start without multiprocessing ')
        result = []
        for sid in sid_list:
            wrap_worker(sid)
            result.append(sid)
    end_time = time.time()

    print(f'{utils.timestamp2formatted(end_time)} : All Jobs finished. It took: {timedelta(seconds=(end_time - start_time))}')
    
