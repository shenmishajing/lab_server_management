import os
import time

import pynvml
import argparse


def get_real_gpus(gpus):
    if isinstance(gpus, int):
        if 'CUDA_VISIBLE_DEVICES' in os.environ:
            gpus = int(os.environ["CUDA_VISIBLE_DEVICES"].split(',')[gpus])
        return gpus
    elif isinstance(gpus, str):
        gpus = [int(g) for g in gpus.split(',')]
    if 'CUDA_VISIBLE_DEVICES' in os.environ:
        gpus = [int(os.environ["CUDA_VISIBLE_DEVICES"].split(',')[gpu]) for gpu in gpus]
    return gpus


def parse_args():
    parser = argparse.ArgumentParser(description = 'use python main.py to occupy gpus')
    parser.add_argument('-gpus', nargs = '+', type = int, default = None, help = 'gpu ids to occupied, default: all gpus')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    pynvml.nvmlInit()
    print('pynvml initialized')

    if args.gpus is None:
        all_gpus = list(range(pynvml.nvmlDeviceGetCount()))
    else:
        all_gpus = get_real_gpus(args.gpus)

    if len(all_gpus) == 0:
        print('no gpus, exit')
        return

    for gpu in all_gpus:
        start_time = time.time()
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_name = pynvml.nvmlDeviceGetName(handle).decode('utf8')
        end_time = time.time()
        print(f'get memory info of {gpu} {gpu_name} in {end_time - start_time}s')
        # time.sleep(2)


if __name__ == "__main__":
    main()
