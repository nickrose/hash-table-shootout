import sys
import subprocess
import numpy as np
from tqdm import tqdm

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

minkeys = 2*100*1000
maxkeys = 30*100*1000
interval = 2*100*1000
best_out_of = 5

debug = 0
outfile = open('output_results.txt', 'w')
outfile_all_stats = open('output_results.stats.txt', 'w')

if len(sys.argv) > 1:
    benchtypes = sys.argv[1:]
else:
    benchtypes = ['insert_random_shuffle_range', 'read_random_shuffle_range',
                  'insert_random_full', 'insert_random_full_reserve',
                  'read_random_full', 'read_miss_random_full',
                  'read_random_full_after_delete',
                  'iteration_random_full', 'delete_random_full',

                  'insert_small_string', 'insert_small_string_reserve',
                  'read_small_string', 'read_miss_small_string',
                  'read_small_string_after_delete',
                  'delete_small_string',

                  'insert_string', 'insert_string_reserve',
                  'read_string', 'read_miss_string',
                  'read_string_after_delete',
                  'delete_string']

nkeys_range = range(minkeys, maxkeys + 1, interval)
if debug == 0:
    iter_display = tqdm(total=len(programs) * len(nkeys_range) * len(benchtypes))
count = 0
for nkey_idx, nkeys in enumerate(nkeys_range):
    for benchtype in benchtypes:
        for program in programs:
            if debug == 0:
                iter_display.set_description((f'nkeys[{nkeys}] test[{benchtype}] '
                    f'program[{program}]'))
                iter_display.update(count)
                count += 1
            if program.startswith('tsl_array_map') and 'string' not in benchtype:
                continue

            fastest_attempt = np.inf
            fastest_attempt_data = ''

            rt_attempts = np.nan * np.ones(best_out_of)
            mu_attempts = np.nan * np.ones(best_out_of)
            lf_attempts = np.nan * np.ones(best_out_of)
            for attempt in range(best_out_of):
                try:
                    output = subprocess.check_output(
                        ['./build/' + program, str(nkeys), benchtype])
                    words = output.strip().split()

                    runtime_seconds = float(words[0])
                    memory_usage_bytes = int(words[1])
                    load_factor = float(words[2])
                except:
                    if debug:
                        print("Error with %s" % str(['./build/' + program, str(nkeys), benchtype]))
                    break

                rt_attempts[attempt] = np.round(runtime_seconds * 1e7) * 1e-7
                mu_attempts[attempt] = memory_usage_bytes
                lf_attempts[attempt] = np.round(load_factor * 1e3) * 1e-3

                if runtime_seconds < fastest_attempt:
                    fastest_attempt = runtime_seconds
                    fastest_attempt_data = ','.join(
                        map(str, [benchtype, nkeys, program, load_factor,
                            memory_usage_bytes, runtime_seconds]))

            if ~np.isinf(fastest_attempt):
                outfile.write(fastest_attempt_data)
                if debug:
                    print(fastest_attempt_data)

                verbose_line = ','.join(map(str, [benchtype, nkeys, program]))
                # load factor
                nonnan = lf_attempts[~np.isnan(rt_attempts)]
                if nonnan.size:
                    _min, mean, std, _max = nonnan.min(), nonnan.mean(), nonnan.std(), nonnan.max()
                    verbose_line += ';' + ','.join(map(str, [_min, mean, std, _max]))
                # memory used
                nonnan = mu_attempts[~np.isnan(rt_attempts)]
                if nonnan.size:
                    _min, mean, std, _max = nonnan.min(), nonnan.mean(), nonnan.std(), nonnan.max()
                    verbose_line += ';' + ','.join(map(str, [_min, mean, std, _max]))
                # runtime seconds
                nonnan = rt_attempts[~np.isnan(rt_attempts)]
                if nonnan.size:
                    _min, mean, std, _max = nonnan.min(), nonnan.mean(), nonnan.std(), nonnan.max()
                    verbose_line += ';' + ','.join(map(str, [_min, mean, std, _max]))

                outfile_all_stats.write(verbose_line)

        # Print blank line
        outfile.write('\n')
        outfile_all_stats.write('\n')
        if debug:
            print('\n')

outfile.close()
outfile_all_stats.close()
