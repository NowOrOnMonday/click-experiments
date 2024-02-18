import time
import sys
from click_sequence_utilities import move_to_delay_click

def do_click_sequence2():
    move_to_delay_click(1368, 109)
    time.sleep(1)
    move_to_delay_click(696, 23)
    time.sleep(1)
    move_to_delay_click(1477, 109)
    time.sleep(1)
    sys.exit()


def do_click_sequence_mint_fhdw():
    move_to_delay_click(1466, 568)
    time.sleep(3)
    move_to_delay_click(1500, 703)
    time.sleep(5)
    move_to_delay_click(1626, 814)
    time.sleep(43)
    move_to_delay_click(1502, 748)
    time.sleep(3)


def click_sequence_minting():
    for i in range(1, 80):
        if i == 79:
            break
        print(i)
        do_click_sequence_mint_fhdw()