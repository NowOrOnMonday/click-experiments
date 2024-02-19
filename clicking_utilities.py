import pyautogui
# from pynput.mouse import Listener, Button
# import os
# import sys
import mouse
import time

run: bool
clicks: list


def on_click(mouse_event) -> None:
    global run
    global clicks
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
                    clicks.append((x, y))
    elif isinstance(mouse_event, mouse.MoveEvent):
        pass
    elif isinstance(mouse_event, mouse.WheelEvent):
        pass
    else:
        pass


def move_delay_click(x: int, y: int, delay: float = 0.5) -> None:
    mouse.move(x, y)
    time.sleep(delay)
    pyautogui.click(x, y)


def click_coordinates(coordinates: list[tuple[int, int]], delay_between_clicks: int) -> None:
    n = len(coordinates)
    for x, y in coordinates:
        print(f'click at {x},{y}')
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        n -= 1
        if n > 0:   # it's not the last click
            print(f'waiting {delay_between_clicks} seconds ...')
            time.sleep(delay_between_clicks)


def learn_clicks() -> list[tuple[int, int]]:
    global run
    global clicks
    print("learning clicks: click left or right\nfinish learning with click in top range of screen")
    clicks = []
    mouse.hook(on_click)
    run = True
    while run:
        mouse.wait()
    mouse.unhook(on_click)
    return clicks


clicks = learn_clicks()
print(f"start clicking at {clicks} in 30 seconds ...")
time.sleep(30)
click_coordinates(clicks, delay_between_clicks=220)
print("finished")
