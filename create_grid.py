from gimpfu import *
import textwrap

def draw_grid(layer, x1, y1, x2, y2):
    pdb.gimp_context_set_foreground((0, 0, 0))  # Set color to black
    pdb.gimp_paintbrush_default(layer, 4, [x1, y1, x2, y1])
    pdb.gimp_paintbrush_default(layer, 4, [x1, y2, x2, y2])
    pdb.gimp_paintbrush_default(layer, 4, [x1, y1, x1, y2])
    pdb.gimp_paintbrush_default(layer, 4, [x2, y1, x2, y2])

def wrap_text(text, width):
    '''Wrap text to specified width.'''
    return textwrap.fill(text, width)

def place_text(image, drawable, x, y, text):
    # Set the font and size
    font_name = "Arial"
    font_size = 40  # Adjust this as needed

    # Wrap the text to fit the grid square
    wrapped_text = wrap_text(text, 25)
    text_layer = pdb.gimp_text_fontname(image, None, 0, 0, wrapped_text, 0, True, font_size, PIXELS, font_name)

    # Find out the width and height of the text layer
    text_width = pdb.gimp_drawable_width(text_layer)
    text_height = pdb.gimp_drawable_height(text_layer)

    # Calculate how much to translate the layer to position the text's center at (x,y)
    translate_x = x - text_width / 2
    translate_y = y - text_height / 2  # Subtracting 10 pixels, adjust as necessary

    pdb.gimp_layer_translate(text_layer, translate_x, translate_y)

    return text_layer  # Return the text layer for any further operations

def create_image():

    gap_in_pixels = 500  # Pixels (10 pixels = 1mm)
    total_size = gap_in_pixels * 3

    # Create a new RGB image
    image = gimp.Image(total_size, total_size, RGB)
    layer = gimp.Layer(image, "Background", total_size, total_size, RGB_IMAGE, 100, NORMAL_MODE)
    image.add_layer(layer, 0)
    gimp.set_background((255, 255, 255))  # Set background color to white
    drawable = pdb.gimp_image_get_active_layer(image)
    pdb.gimp_drawable_fill(drawable, BACKGROUND_FILL)

    draw_grid(drawable, gap_in_pixels, 0, gap_in_pixels, total_size)
    draw_grid(drawable, total_size - gap_in_pixels, 0, total_size - gap_in_pixels, total_size)
    draw_grid(drawable, 0, gap_in_pixels, total_size, gap_in_pixels)
    draw_grid(drawable, 0, total_size - gap_in_pixels, total_size, total_size - gap_in_pixels)

     # Place the text at the center of each grid block
    centers = [
        (gap_in_pixels / 2, gap_in_pixels / 2),           # Top-left square
        (gap_in_pixels * 1.5, gap_in_pixels / 2),         # Top-middle square
        (gap_in_pixels * 2.5, gap_in_pixels / 2),         # Top-right square
        (gap_in_pixels / 2, gap_in_pixels * 1.5),         # Middle-left square
        (gap_in_pixels * 1.5, gap_in_pixels * 1.5),       # Center square
        (gap_in_pixels * 2.5, gap_in_pixels * 1.5),       # Middle-right square
        (gap_in_pixels / 2, gap_in_pixels * 2.5),         # Bottom-left square
        (gap_in_pixels * 1.5, gap_in_pixels * 2.5),       # Bottom-middle square
        (gap_in_pixels * 2.5, gap_in_pixels * 2.5),       # Bottom-right square
    ]

    for center in centers:
        x, y = center
        place_text(image, drawable, x, y, "Text that will be centered in the grid.")

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
