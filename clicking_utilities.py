import pyautogui
# from pynput.mouse import Listener, Button
# import os
# import sys
import mouse
# from mouse import ButtonEvent, MoveEvent, WheelEvent
import time
import cv2 as cv
import numpy as np
from pyautogui import ImageNotFoundException

run: bool
coordinates: list


def on_mouse_event(mouse_event: mouse.ButtonEvent | mouse.MoveEvent | mouse.WheelEvent) -> None:
    global run
    global coordinates
    if isinstance(mouse_event, mouse.ButtonEvent):
        # print("ButtonEvent")
        if mouse_event.event_type == mouse.DOWN:
            x, y = mouse.get_position()
            if y < 10:
                print(f'clicked at ({x},{y}) => cancel')
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


def on_mouse_event_two_clicks(mouse_event: mouse.ButtonEvent | mouse.MoveEvent | mouse.WheelEvent) -> None:
    global run
    global coordinates
    global click_counter
    global event_counter
    event_counter += 1
    print(f"enter on_mouse_event_two_clicks. Event {event_counter}.")
    if isinstance(mouse_event, mouse.ButtonEvent):
        # print("ButtonEvent")
        if mouse_event.event_type == mouse.DOWN:
            x, y = mouse.get_position()
            if y < 10:
                print(f'clicked at ({x},{y}) => cancel')
                run = False
                mouse.unhook(on_mouse_event_two_clicks)
            else:
                # print(f"Current mouse position: x={x}, y={y}")
                # print(f'moveToDelayClick({x}, {y})')
                if isinstance(coordinates, list):
                    coordinates.append((x, y))
                    click_counter += 1
                    print(f"learned ({x},{y})  {click_counter = }")
                    if click_counter == 2:
                        print("set run = False")
                        run = False
                        mouse.unhook(on_mouse_event_two_clicks)
    elif isinstance(mouse_event, mouse.MoveEvent):
        pass
    elif isinstance(mouse_event, mouse.WheelEvent):
        pass
    else:
        pass
    print(f"exit on_mouse_event_two_clicks. Event {event_counter}.")


def save_region_as_png(file_path: str, coordinates: list[tuple[int, int]]) -> bool:
    assert len(coordinates) == 2
    x1 = coordinates[0][0]
    x2 = coordinates[1][0]
    y1 = coordinates[0][1]
    y2 = coordinates[1][1]
    x_min = min(x1, x2)
    y_min = min(y1, y2)
    x_max = max(x1, x2)
    y_max = max(y1, y2)
    w = x_max - x_min
    h = y_max - y_min
    if w == 0 or h == 0:
        return False
    pilimg = pyautogui.screenshot(region=(x_min, y_min, w, h))  # return an Image object (Pillow, PIL)
    cvimage = cv.cvtColor(np.array(pilimg), cv.COLOR_RGB2BGR)
    cv.imshow("cvimage", cvimage)
    cv.imwrite(file_path, cvimage)
    return True


def save_region_as_png_by_two_clicks(file_path: str) -> None:
    global run
    global coordinates
    global click_counter
    global event_counter
    print(f"two clicks to define region to save as {file_path}. click in top range of screen to cancel.")
    coordinates = []
    click_counter = 0
    event_counter = 0
    run = True
    mouse.hook(on_mouse_event_two_clicks)
    while run:
        print("while body begin")
        print(f"waiting for mouse click {click_counter + 1} ...")
        mouse.wait()
        print("while body end")
    print("while loop left")
    # mouse.unhook(on_mouse_event_two_clicks)
    if click_counter == 2:
        assert len(coordinates) == 2
        save_region_as_png(file_path, coordinates)
    else:
        print("no image saved.")


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
    run = True
    mouse.hook(on_mouse_event)
    while run:
        print("start while ...")
        mouse.wait()
    mouse.unhook(on_mouse_event)
    return coordinates


def get_center_coordinate_of_image(image_path: str) -> None | tuple[int, int]:
    try:
        coordinate = pyautogui.locateCenterOnScreen(image_path, confidence=0.99)
        result = (coordinate.x, coordinate.y)
    except ImageNotFoundException:
        result = None
    # print(f'{result = }')
    return result


def main() -> None:
    result_coordinates = learn_coordinates()
    initial_wait_time = 10
    delay_between_clicks = 220
    print(f"start clicking at {result_coordinates} in {initial_wait_time} seconds ...")
    time.sleep(initial_wait_time)
    click_at_coordinates(result_coordinates, delay_between_clicks=delay_between_clicks)
    print("finished main")


def main2() -> None:
    # save_region_as_png("/tmp/image.png", [(10, 20), (100, 200)])
    save_region_as_png_by_two_clicks("/tmp/image.png")
    print("finished main2")


if __name__ == "__main__":
    png_image_path = "assets/buttonAlleBeenden.png"
    png_image_path = "assets/buttonAllesAbholen.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        # result = get_center_coordinate_of_image()
        print(f'center of {png_image_path} at ({x}, {y}).')
        mouse.move(x, y)
    else:
        print(f"{png_image_path} not found")
