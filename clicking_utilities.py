import pyautogui
# from pynput.mouse import Listener, Button
# import os
# import sys
import mouse
# from mouse import ButtonEvent, MoveEvent, WheelEvent
import time

run: bool
coordinates: list


def on_click(mouse_event: mouse.ButtonEvent | mouse.MoveEvent | mouse.WheelEvent) -> None:
    global run
    global coordinates
    if isinstance(mouse_event, mouse.ButtonEvent):
        # print("ButtonEvent")
        if mouse_event.event_type == mouse.DOWN:
            x, y = mouse.get_position()
            if y < 10:
                run = False
            else:
                # print(f"Current mouse position: x={x}, y={y}")
                # print(f'moveToDelayClick({x}, {y})')
                if isinstance(coordinates, list):
                    print(f'learned ({x},{y})')
                    coordinates.append((x, y))
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


def click_at_coordinates(p_coordinates: list[tuple[int, int]], delay_between_clicks: int) -> None:
    n = len(p_coordinates)
    for x, y in p_coordinates:
        print(f'click at {x},{y}')
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        n -= 1
        if n > 0:   # it's not the last click
            print(f'waiting {delay_between_clicks} seconds ...')
            time.sleep(delay_between_clicks)


def learn_coordinates() -> list[tuple[int, int]]:
    global run
    global coordinates
    print("learning clicks: click left or right\nfinish learning with click in top range of screen")
    coordinates = []
    mouse.hook(on_click)
    run = True
    while run:
        mouse.wait()
    mouse.unhook(on_click)
    return coordinates


def main() -> None:
    result_coordinates = learn_coordinates()
    initial_wait_time = 10
    delay_between_clicks = 220
    print(f"start clicking at {result_coordinates} in {initial_wait_time} seconds ...")
    time.sleep(initial_wait_time)
    click_at_coordinates(result_coordinates, delay_between_clicks=delay_between_clicks)
    print("finished")


main()
