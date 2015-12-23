import subprocess
import time
import urllib

import numpy as np

from stbt import press, wait_until, match, Region


black_rect = np.empty((8, 8, 3), dtype=np.uint8)
black_rect.fill(16)
region = Region(0, 0, width=8, height=8)


def test_motorola():
    subprocess.call(['free', '-m'])
    with open('results_file', 'w') as results_file:
        for _ in range(10000):
            ir_left_start = time.time()
            press('KEY_LEFT')
            ir_left_end = time.time()
            if wait_until(lambda: match(black_rect, region=region), timeout_secs=3):
                match_found = time.time()
            else:
                match_found = -1
            ir_right_start = time.time()
            press('KEY_RIGHT')
            ir_right_end = time.time()
            if wait_until(lambda: not match(black_rect, region=region), timeout_secs=3):
                match_disappeared = time.time()
            else:
                match_disappeared = -1
            line = '{0:f} {1:f} {2:f} {3:f} {4:f} {5:f}\n'.format(
                ir_left_start,
                ir_left_end,
                match_found,
                ir_right_start,
                ir_right_end,
                match_disappeared
            )
            results_file.write(line)
    subprocess.call(['free', '-m'])
