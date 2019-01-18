""" Script to execute benchmarking tests on various hash table implementations

    execute using
        python bench.py

    Nick Roseveare, Jan 2019
"""
import sys
import subprocess
import numpy as np
from tqdm import tqdm
import os

programs = [
    # 'std_unordered_map',
    'boost_unordered_map',
    'google_sparse_hash_map',
    'google_dense_hash_map',
    'google_dense_hash_map_mlf_0_9',
    'libcuckoo_map',
    'qt_qhash',
    'spp_sparse_hash_map',
    # 'emilib_hash_map',
    # 'ska_flat_hash_map',
    # 'ska_flat_hash_map_power_of_two',
    'tsl_sparse_map',
    'tsl_hopscotch_map',
    'tsl_hopscotch_map_mlf_0_5',
    'tsl_hopscotch_map_store_hash',
    'tsl_robin_map',
    'tsl_robin_map_mlf_0_9',
    'tsl_robin_map_store_hash',
    'tsl_robin_pg_map',
    'tsl_ordered_map',
    'tsl_array_map',
    'tsl_array_map_mlf_1_0'
]

newcsvfile = True

base_size = int(1e5)
minkeys = 2 * base_size
maxkeys = 30 * base_size
interval = 2 * base_size
best_out_of = 10

debug = 0
# we have a small file for the minimum runtimes/usages found, and another for
# with more statistics
# outfile = 'modified_cuckoo_compare.csv'
# outfile_all_stats = 'modified_cuckoo_compare.stats.csv'
outfile = 'output_results.csv'
outfile_all_stats = 'output_results.stats.csv'

if len(sys.argv) > 1:
    benchtypes = sys.argv[1:]
else:
    benchtypes = [

        # 'insert_random_shuffle_range_reserve',
        'insert_random_full_reserve',

        # 'read_random_shuffle_range_reserve',
        # 'read_random_full_reserve',
        # 'read_miss_random_full_reserve',
        # 'read_random_full_after_delete_reserve',

        # 'delete_random_full_reserve',

        # 'iteration_random_full_reserve'

        'insert_random_shuffle_range',
        'insert_random_full',

        'read_random_shuffle_range',
        'read_random_full',
        'read_miss_random_full',
        'read_random_full_after_delete',

        'delete_random_full',

        'iteration_random_full'


        'insert_string',
        'insert_string_reserve',
        'insert_small_string',
        'insert_small_string_reserve',

        'read_string',
        'read_miss_string',
        'read_string_after_delete',
        'read_small_string',
        'read_miss_small_string',
        'read_small_string_after_delete',

        'delete_string',
        'delete_small_string',

    ]

nkeys_range = range(maxkeys, minkeys-1, -interval)
total = (len(programs) * len(nkeys_range) * len(benchtypes))
if debug == 0:
    progress_bar = tqdm(total=total)
count = 0
if total > 0:
    if newcsvfile or not(os.path.isfile(outfile)):
        with open(outfile, 'w') as file:
            file.write(('test_type, nkeys, hash_table_algo, lf_min, mem_bytes_min, '
                'runtime_sec_min'))
            file.write('\n')
    if newcsvfile or not(os.path.isfile(outfile_all_stats)):
        with open(outfile_all_stats, 'w') as file:
            file.write(
                'test_type, nkeys, hash_table_algo, lf_min, lf_avg, lf_std, lf_max, '
                'mem_bytes_min, mem_bytes_avg, mem_bytes_std, mem_bytes_max, '
                'runtime_sec_min, runtime_sec_avg, runtime_sec_std, runtime_sec_max')
            file.write('\n')

rt_attempts = np.nan * np.ones(best_out_of, dtype=float)
mu_attempts = np.nan * np.ones(best_out_of, dtype=int)
lf_attempts = np.nan * np.ones(best_out_of, dtype=float)

for nkey_idx, nkeys in enumerate(nkeys_range):
    for benchtype in benchtypes:
        for program in programs:
            if debug == 0:
                count += 1
                progress_bar.n = count
                progress_bar.set_description((
                    f'nkeys[{nkeys}] '
                    f'test[{benchtype}] '
                    f'program[{program}]'))
            if program.startswith('tsl_array_map') and 'string' not in benchtype:
                continue

            fastest_attempt = np.inf
            fastest_attempt_data = ''

            rt_attempts[:] = np.nan
            mu_attempts[:] = np.nan
            lf_attempts[:] = np.nan
            for attempt in range(best_out_of):
                try:
                    output = subprocess.check_output(
                        ['./build/' + program, str(nkeys), benchtype])
                    words = output.strip().split()

                    runtime_seconds = float(words[0])
                    memory_usage_bytes = int(words[1])
                    load_factor = float(words[2])
                except KeyboardInterrupt:
                    sys.exit(1)
                except:
                    if debug:
                        print((f"Error with {('./build/' + program)}"
                            f"[{nkeys}: {benchtype}]"))
                    break

                rt_attempts[attempt] = np.round(runtime_seconds, decimals=7)
                mu_attempts[attempt] = memory_usage_bytes
                lf_attempts[attempt] = np.round(load_factor, decimals=3)

                if runtime_seconds < fastest_attempt:
                    fastest_attempt = runtime_seconds
                    fastest_attempt_data = ','.join(
                        map(str, [benchtype, nkeys, program, load_factor,
                            memory_usage_bytes, runtime_seconds]))

            if ~np.isinf(fastest_attempt):

                with open(outfile, 'a') as file:
                    file.write(fastest_attempt_data)
                    # Print blank line
                    file.write('\n')

                if debug:
                    print(fastest_attempt_data)

                verbose_line = ','.join(map(str, [benchtype, nkeys, program]))
                # load factor
                nonnan = lf_attempts[~np.isnan(rt_attempts)]
                if nonnan.size:
                    _min, mean, std, _max = (nonnan.min(), nonnan.mean(),
                        nonnan.std(), nonnan.max())
                    verbose_line += ',' + ','.join(map(str,
                        [_min, mean, std, _max]))
                # memory used
                nonnan = mu_attempts[~np.isnan(rt_attempts)]
                if nonnan.size:
                    _min, mean, std, _max = (nonnan.min(), nonnan.mean(),
                        nonnan.std(), nonnan.max())
                    verbose_line += ',' + ','.join(map(str,
                        [_min, mean, std, _max]))
                # runtime seconds
                nonnan = rt_attempts[~np.isnan(rt_attempts)]
                if nonnan.size:
                    _min, mean, std, _max = (nonnan.min(), nonnan.mean(),
                        nonnan.std(), nonnan.max())
                    verbose_line += ',' + ','.join(map(str,
                        [_min, mean, std, _max]))

                with open(outfile_all_stats, 'a') as file:
                    file.write(verbose_line)
                    file.write('\n')

            if debug:
                print('\n')
