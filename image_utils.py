from PIL import Image


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

def cut_image(png_image_path: str, top_rows: int, bottom_rows: int, left_columns: int, right_columns: int) -> None:
    for i in range(top_rows):
        remove_row(png_image_path, 0)
    for i in range(bottom_rows):
        remove_row(png_image_path, -1)
    for i in range(left_columns):
        remove_column(png_image_path, 0)
    for i in range(right_columns):
        remove_column(png_image_path, -1)