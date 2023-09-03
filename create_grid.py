from gimpfu import *
import textwrap

def mm_to_pixels(mm, dpi=300): # Using 300 DPI by default
    return int(mm * dpi / 25.4)

def draw_grid(layer, x1, y1, x2, y2):
    pdb.gimp_context_set_foreground((0, 0, 0))  # Set color to black
    pdb.gimp_paintbrush_default(layer, 4, [x1, y1, x2, y1])
    pdb.gimp_paintbrush_default(layer, 4, [x1, y2, x2, y2])
    pdb.gimp_paintbrush_default(layer, 4, [x1, y1, x1, y2])
    pdb.gimp_paintbrush_default(layer, 4, [x2, y1, x2, y2])

def wrap_text(text, width):
    '''Wrap text to specified width.'''
    return textwrap.fill(text, width)

def place_text(image, x, y, text):
    # Set the font and size
    font_name = "Arial"
    font_size = 40  # Adjust this as needed

    # Wrap the text to fit the grid square
    wrapped_text = wrap_text(text, 15)
    text_layer = pdb.gimp_text_fontname(image, None, 0, 0, wrapped_text, 0, True, font_size, PIXELS, font_name)

    # Find out the width and height of the text layer
    text_width = pdb.gimp_drawable_width(text_layer)
    text_height = pdb.gimp_drawable_height(text_layer)

    # Calculate how much to translate the layer to position the text's center at (x,y)
    translate_x = x - text_width / 2
    translate_y = y - text_height / 2

    pdb.gimp_layer_translate(text_layer, translate_x, translate_y)

    return text_layer  # Return the text layer for any further operations

def create_image():

    width_in_mm = 29
    height_in_mm = 36
    gap_in_pixels_width = mm_to_pixels(width_in_mm)
    gap_in_pixels_height = mm_to_pixels(height_in_mm)

    total_size_width = gap_in_pixels_width * 3
    total_size_height = gap_in_pixels_height * 3

    # Create a new RGB image
    image = gimp.Image(total_size_width, total_size_height, RGB)
    layer = gimp.Layer(image, "Background", total_size_width, total_size_height, RGB_IMAGE, 100, NORMAL_MODE)
    image.add_layer(layer, 0)
    gimp.set_background((255, 255, 255))  # Set background color to white
    drawable = pdb.gimp_image_get_active_layer(image)
    pdb.gimp_drawable_fill(drawable, BACKGROUND_FILL)

    draw_grid(drawable, gap_in_pixels_width, 0, gap_in_pixels_width, total_size_height)
    draw_grid(drawable, total_size_width - gap_in_pixels_width, 0, total_size_width - gap_in_pixels_width, total_size_height)
    draw_grid(drawable, 0, gap_in_pixels_height, total_size_width, gap_in_pixels_height)
    draw_grid(drawable, 0, total_size_height - gap_in_pixels_height, total_size_width, total_size_height - gap_in_pixels_height)

     # Place the text at the center of each grid block
    centers = [
        (gap_in_pixels_width  / 2, gap_in_pixels_height  / 2),           # Top-left square
        (gap_in_pixels_width  * 1.5, gap_in_pixels_height  / 2),         # Top-middle square
        (gap_in_pixels_width  * 2.5, gap_in_pixels_height  / 2),         # Top-right square
        (gap_in_pixels_width  / 2, gap_in_pixels_height  * 1.5),         # Middle-left square
        (gap_in_pixels_width  * 1.5, gap_in_pixels_height  * 1.5),       # Center square
        (gap_in_pixels_width  * 2.5, gap_in_pixels_height  * 1.5),       # Middle-right square
        (gap_in_pixels_width  / 2, gap_in_pixels_height  * 2.5),         # Bottom-left square
        (gap_in_pixels_width  * 1.5, gap_in_pixels_height  * 2.5),       # Bottom-middle square
        (gap_in_pixels_width  * 2.5, gap_in_pixels_height  * 2.5),       # Bottom-right square
    ]

    for center in centers:
        x, y = center
        place_text(image, x, y, "STOP! Think before you scan!")

    # Display the image
    gimp.Display(image)
    gimp.displays_flush()

register(
    "python_fu_create_image",
    "Create a Grid Image",
    "Create a new image with grid",
    "Your Name",
    "Your Name",
    "2023",
    "Create Grid Image added function added draw text...",
    "",
    [],
    [],
    create_image,
    menu="<Image>/File/Create"
)

main()
