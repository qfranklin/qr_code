from gimpfu import *

def draw_grid(image, layer, x1, y1, x2, y2):
    pdb.gimp_context_set_foreground((0, 0, 0))  # Set color to black
    pdb.gimp_paintbrush_default(layer, 4, [x1, y1, x2, y1])
    pdb.gimp_paintbrush_default(layer, 4, [x1, y2, x2, y2])
    pdb.gimp_paintbrush_default(layer, 4, [x1, y1, x1, y2])
    pdb.gimp_paintbrush_default(layer, 4, [x2, y1, x2, y2])

def create_image():

    gap_in_pixels = 430  # Pixels (10 pixels = 1mm)
    total_size = gap_in_pixels * 3

    # Create a new RGB image
    image = gimp.Image(total_size, total_size, RGB)
    layer = gimp.Layer(image, "Background", total_size, total_size, RGB_IMAGE, 100, NORMAL_MODE)
    image.add_layer(layer, 0)
    gimp.set_background((255, 255, 255))  # Set background color to white
    drawable = pdb.gimp_image_get_active_layer(image)
    pdb.gimp_drawable_fill(drawable, BACKGROUND_FILL)

    draw_grid(image, drawable, gap_in_pixels, 0, gap_in_pixels, total_size)
    draw_grid(image, drawable, total_size - gap_in_pixels, 0, total_size - gap_in_pixels, total_size)
    draw_grid(image, drawable, 0, gap_in_pixels, total_size, gap_in_pixels)
    draw_grid(image, drawable, 0, total_size - gap_in_pixels, total_size, total_size - gap_in_pixels)

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
    "Create Grid Image...",
    "",
    [],
    [],
    create_image,
    menu="<Image>/File/Create"
)

main()
