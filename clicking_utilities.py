import pyautogui
# from pynput.mouse import Listener, Button
# import os
import sys
import mouse
# from mouse import ButtonEvent, MoveEvent, WheelEvent
import time
import cv2 as cv
import numpy as np
from pyautogui import ImageNotFoundException
from PIL import Image


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
        if save_region_as_png(file_path, coordinates):
            print(f"image saved as {file_path}.")
        else:
            print(f"image NOT saved ({file_path}).")
    else:
        print("no image saved.")


def remove_row(image_path: str, row_number: int) -> None:
    image = Image.open(image_path)
    width, height = image.size
    if row_number < 0:
        row_number = height + row_number
    if row_number < 0 or row_number >= height:
        print(f"error: invalid row index {row_number}. Image height is {height}.")
        return
    else:
        pixels = list(image.getdata())
        new_pixels = [pixels[i * width:(i + 1) * width] for i in range(height) if i != row_number]
        new_data = [pixel for row in new_pixels for pixel in row]
        new_image = Image.new(image.mode, (width, height - 1))
        new_image.putdata(new_data)
        new_image.save(f"{image_path}")


def remove_column(image_path, column_number):
    image = Image.open(image_path)
    width, height = image.size
    if column_number < 0:
        column_number = width + column_number
    if column_number < 0 or column_number >= width:
        print(f"error: invalid row index {column_number}. Image width is {width}.")
        return
    else:
        pixels = list(image.getdata())
        new_pixels = [pixels[i*width:i*width+column_number] + pixels[i*width+column_number+1:(i+1)*width] for i in range(height)]
        new_data = [pixel for row in new_pixels for pixel in row]
        new_image = Image.new(image.mode, (width - 1, height))
        new_image.putdata(new_data)
        new_image.save(f"{image_path}")


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


def get_top_left_coordinate_of_factory(factory_id: int) -> None | tuple[int, int]:
    if factory_id not in [1,2,3,4,5,6]:
        result = None
        print(f'factory {factory_id} not found.')
    else:
        try:
            image_path  = "assets/iconFabriken.png"
            coordinate = pyautogui.locateCenterOnScreen(image_path, confidence=0.99)
            x, y = coordinate.x-201, coordinate.y+34   # factory 1
            offsets = [(0, 0), (150, 0), (300, 0), (0, 200), (150, 200), (300, 200)]
            result = (x + offsets[factory_id-1][0], y + offsets[factory_id-1][1])
        except ImageNotFoundException:
            result = None
    return result


def click_on_factory(factory_id: int) -> bool:
    coord = get_top_left_coordinate_of_factory(factory_id)
    if coord:
        x, y = coord
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(1)
        result = True
        print(f'clicked on factory {factory_id}.')
    else:
        result = False
        print(f'factory {factory_id} not found.')
    return result


def click_on_button_repair_factory(factory_id: int) -> bool:
    coord = get_top_left_coordinate_of_factory(factory_id)
    if coord:
        x, y = coord
        x, y = x + 108, y + 141
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(1)
        result = True
        print(f'clicked on repair factory {factory_id}.')
    else:
        result = False
        print(f'repair button of factory {factory_id} not found. no click.')
    return result


def click_on_button_AllesAbholen_if_present() -> bool:
    png_image_path = "assets/buttonAllesAbholen.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_AllesProduzieren_if_present() -> None:
    png_image_path = "assets/buttonAllesProduzieren.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_Close_if_present() -> None:
    png_image_path = "assets/buttonClose.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_GotoPreviousPane_if_present() -> None:
    png_image_path = "assets/buttonGotoPreviousPane.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        mouse.move(0, 0)
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_GotoNextPane_if_present() -> None:
    png_image_path = "assets/buttonGotoNextPane.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        mouse.move(0, 0)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_OpenWarehouse_if_present() -> None:
    png_image_path = "assets/buttonOpenWarehouse.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        mouse.move(0, 0)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_GotoNextIconSet_if_present() -> None:
    png_image_path = "assets/buttonGotoNextIconSet.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        mouse.move(0, 0)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_EnterArtistInWarehouse_if_present() -> None:
    png_image_path = "assets/buttonEnterArtistInWarehouse.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        mouse.move(0, 0)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_area_UpDownNumberToDelete() -> None:
    png_image_path = "assets/areaUpDownNumberToDelete.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_button_Wegwerfen_if_present() -> None:
    png_image_path = "assets/buttonWegwerfen.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        mouse.move(0, 0)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def click_on_area_FactoryOverview_if_present() -> None:
    png_image_path = "assets/areaFactoryOverview.png"
    result = get_center_coordinate_of_image(png_image_path)
    if result:
        x = result[0]
        y = result[1]
        mouse.move(x, y)
        time.sleep(0.5)
        pyautogui.click(x, y)
        mouse.move(0, 0)
        print(f'clicked on {png_image_path} at ({x}, {y}).')
        result = True
    else:
        print(f"{png_image_path} not found. no click.")
        result = False
    return result


def typewrite(s: str) -> None:
    pyautogui.typewrite(s, interval=0.3)


def learn_and_click() -> None:
    result_coordinates = learn_coordinates()
    initial_wait_time = 10
    delay_between_clicks = 220
    print(f"start clicking at {result_coordinates} in {initial_wait_time} seconds ...")
    time.sleep(initial_wait_time)
    click_at_coordinates(result_coordinates, delay_between_clicks=delay_between_clicks)
    print("finished main")


def fetch_goods_from_current_pane():
    for factory_id in range(1, 7):
        if click_on_factory(factory_id):
            time.sleep(2)
            click_on_button_AllesAbholen_if_present()
            time.sleep(2)
            click_on_button_repair_factory(factory_id)
            time.sleep(2)
            click_on_button_AllesProduzieren_if_present()
        else:
            print(f'factory {factory_id} not found.')
        time.sleep(2)


def main3() -> None:
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


def cut_image(png_image_path: str, top_rows: int, bottom_rows: int, left_columns: int, right_columns: int) -> None:
    for i in range(top_rows):
        remove_row(png_image_path, 0)
    for i in range(bottom_rows):
        remove_row(png_image_path, -1)
    for i in range(left_columns):
        remove_column(png_image_path, 0)
    for i in range(right_columns):
        remove_column(png_image_path, -1)


def main4() -> None:
    # click_on_button_Close_if_present()
    click_on_button_GotoNextPane_if_present()
    time.sleep(3)
    click_on_button_GotoPreviousPane_if_present()
    time.sleep(3)
    click_on_button_Close_if_present()
    time.sleep(3)



def enter_factory_overview() -> None:
    click_on_area_FactoryOverview_if_present()
    time.sleep(3)


def enter_warehouse_and_delete_farbpaletten() -> None:
    if click_on_button_OpenWarehouse_if_present():
        time.sleep(5)
        click_on_button_GotoNextIconSet_if_present()
        time.sleep(5)
        click_on_button_GotoNextIconSet_if_present()
        time.sleep(5)
        if click_on_button_EnterArtistInWarehouse_if_present():
            time.sleep(5)
            click_on_area_UpDownNumberToDelete()
            time.sleep(5)
            typewrite("99999")
            time.sleep(5)
            click_on_button_Wegwerfen_if_present()
            time.sleep(3)
            click_on_button_Close_if_present()
            time.sleep(3)
    else:
        print("can't find warehouse button. no click.")


def navigate_to_pane(pane_number: int) -> None:
    while pane_number > 1:
        click_on_button_GotoNextPane_if_present()
        pane_number -= 1
        if pane_number > 1:
            time.sleep(1)


def fetch_color_palettes():
    n_rounds = 0
    while True:
        n_rounds += 1
        print(f"=== starting round {n_rounds} ===")
        enter_factory_overview()
        time.sleep(3)
        navigate_to_pane(5)  # first artist pane
        time.sleep(3)
        for _ in range(2):
            fetch_goods_from_current_pane()
            time.sleep(3)
            click_on_button_GotoNextPane_if_present()
            time.sleep(3)
            fetch_goods_from_current_pane()
            time.sleep(3)
            click_on_button_GotoNextPane_if_present()
            time.sleep(3)
            fetch_goods_from_current_pane()
            time.sleep(3)
            click_on_button_GotoPreviousPane_if_present()
            time.sleep(3)
            click_on_button_GotoPreviousPane_if_present()
            time.sleep(3)
        click_on_button_Close_if_present()
        time.sleep(3)
        enter_warehouse_and_delete_farbpaletten()
        time.sleep(3)
        print(f"--- finished round {n_rounds} ---")


if __name__ == "__main__":
    fetch_color_palettes()
    # learn_and_click()
    # save_region_as_png_by_two_clicks("assets/newImage.png")()
    # click_on_button_Close_if_present()
    # cut_image("assets/dummy.png", 7, 0, 0, 0)
