import pyautogui
# from pynput.mouse import Listener, Button
# import os
import sys
import mouse
import time

run: bool
clicks: list

def on_click(mouse_event):
    global run
    global clicks
    # if pressed:
    # print(f"Mouse clicked at x={x}, y={y} with {button}")
    if isinstance(mouse_event, mouse.ButtonEvent):
        # print("ButtonEvent")
        if mouse_event.event_type == mouse.DOWN:
            x, y = mouse.get_position()
            if y < 10:
                run = False
            else:
                # print(f"Current mouse position: x={x}, y={y}")
                # print(f'moveToDelayClick({x}, {y})')
                if isinstance(clicks, list):
                    print(f'learned ({x},{y})')
                    clicks.append((x,y))
    elif isinstance(mouse_event, mouse.MoveEvent):
        # print("MoveEvent")
        # print(".", end="")
        # print(f'click position: {pyautogui.position()}')
        # print(f'position: {pyautogui.position()}')
        # print(f'move position: {mouse_event.x} {mouse_event.y}')
        pass
    elif isinstance(mouse_event, mouse.WheelEvent):
        # print("WheelEvent")
        pass
    else:
        # print("Other event")
        pass

def moveToDelayClick(x, y, delay=0.5):
    mouse.move(x, y)
    time.sleep(delay)
    pyautogui.click(x, y)


def doClickSequence2():
    moveToDelayClick(1368, 109)
    time.sleep(1)
    moveToDelayClick(696, 23)
    time.sleep(1)
    moveToDelayClick(1477, 109)
    time.sleep(1)
    sys.exit()

def doClickSequenceMintFHDW():
    moveToDelayClick(1466, 568)
    time.sleep(3)
    moveToDelayClick(1500, 703)
    time.sleep(5)
    moveToDelayClick(1626, 814)
    time.sleep(43)
    moveToDelayClick(1502, 748)
    time.sleep(3)


def clickSequenceMinting():
    for i in range(1, 80):
        if i == 79:
            break
        print(i)
        doClickSequenceMintFHDW()


def doClickSequence(clicks, delay_between_clicks):
    n = len(clicks)
    for x, y in clicks:
        print(f'do click at {x},{y}')
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        n -= 1
        if n > 0:   # it's not the last click
            print(f'waiting {delay_between_clicks} seconds ...')
            time.sleep(delay_between_clicks)


def learnClicks() -> list:
    global run
    global clicks
    print("learning clicks ...\nFinish with click at top line.")
    clicks = []
    mouse.hook(on_click)
    run = True
    while run:
        mouse.wait()
    mouse.unhook(on_click)
    return clicks


clicks = learnClicks()
print(f"start clicking at {clicks} in 30 seconds ...")
time.sleep(30)
doClickSequence(clicks, delay_between_clicks=220)
print("finished")

