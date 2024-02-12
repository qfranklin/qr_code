import math
import bpy
import datetime
import os
import sys
import importlib
import qrcode
import qrcode.image.svg

# TODO: get this sensitive data into a secure file
CURRENT_DIR = "C:\\Users\\qfran\\Desktop\\code\\qr_code\\"

# Add the path to your scripts to sys.path
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

import config
import utils 

importlib.reload(config)
importlib.reload(utils)
     
current_time = utils.start()

# Calculate the grid size
grid_size = int(len(config.INPUT_QR_STRINGS)**0.5) + (1 if (len(config.INPUT_QR_STRINGS)**0.5) % 1 > 0 else 0)  # Ceiling of the square root

for index, input_string in enumerate(config.INPUT_QR_STRINGS):

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # Adjust version as needed
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(config.INPUT_QR_STRINGS[index])
    qr.make(fit=True)

    # Create an SVG image factory
    factory = qrcode.image.svg.SvgPathImage

    # Generate the SVG QR code
    svg_image = qr.make_image(image_factory=factory)

    # Create the svg file
    with open(CURRENT_DIR + "input/qrcode.svg", "wb") as f:
        svg_image.save(f)

    # Get a set of current collections before importing
    current_collections = set(bpy.data.collections.keys())

    bpy.ops.import_curve.svg(filepath=CURRENT_DIR + "input\\qrcode.svg")

    # Copy the svg object from the collection to the scene
    qrcode_collection = bpy.data.collections.get("qrcode.svg")
    qrcode_object = qrcode_collection.objects[0]
    bpy.context.scene.collection.objects.link(qrcode_object)

    # Delete the collection
    bpy.data.collections.remove(qrcode_collection)

    qrcode_object.select_set(True)
    bpy.context.view_layer.objects.active = qrcode_object
    bpy.ops.object.convert(target='MESH')

    # Calculate and apply scale factor
    scale_factor = config.QR_CODE_SIZE / max(bpy.context.view_layer.objects.active.dimensions)
    bpy.context.view_layer.objects.active.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    image_obj = bpy.context.view_layer.objects.active

    collection = image_obj.users_collection[0]

    merged_object = utils.center_object(utils.merge_objects(collection))
    utils.solidify_object(not config.INVERT_QR_CODE, config.QR_CODE_THICKNESS)

    # Add baseplate to qr code
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.dimensions = (image_obj.dimensions.x + config.QUIET_ZONE, image_obj.dimensions.y + config.QUIET_ZONE, 1)

    utils.solidify_object(config.INVERT_QR_CODE, config.BASEPLATE_THICKNESS)

    merged_object = utils.center_object(utils.merge_objects(collection))
    bpy.context.view_layer.objects.active = merged_object
    bpy.ops.transform.rotate(value=3.14159, orient_axis='Y')

    image_obj.location = (0, 0, 0)

    # Calculate position in the grid
    i = index // grid_size  # integer division gives the row number
    j = index % grid_size   # modulo gives the column number

    # Position the qr code in the grid
    offset_y = i * (image_obj.dimensions.y + config.QR_SPACING)
    offset_x = j * (image_obj.dimensions.x + config.QR_SPACING)
    image_obj.location.x += offset_x
    image_obj.location.y += offset_y

    image_obj.location = (0, 0, config.QR_CODE_THICKNESS + config.BASEPLATE_THICKNESS)

    if(not config.INVERT_QR_CODE):
        image_obj.rotation_euler.y += math.radians(180)

    print(f"Width: {image_obj.dimensions.x}")
    print(f"Height: {image_obj.dimensions.y}")

    if config.ADD_SD_CARD:
        # Import the pre built sd card stl file
        bpy.ops.import_mesh.stl(filepath = CURRENT_DIR + "input/sd_card.stl")

        sd_card = bpy.context.active_object

        sd_card.location.x = config.QR_CODE_SIZE - 16.5
        sd_card.location.y = -(config.QR_CODE_SIZE - 2)
        sd_card.location.z = .1

        # Add footer plate
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(-9.5, -30.55, .1))
        footer_plate = bpy.context.active_object
        footer_plate.dimensions = (28, 14.7, 1)
        # image_obj.users_collection[0].objects.link(footer_plate)
        # bpy.context.collection.objects.unlink(footer_plate)
        utils.solidify_object(not config.INVERT_QR_CODE, config.BASEPLATE_THICKNESS)

        bpy.ops.object.select_all(action='DESELECT')

        font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
        font_curve.body = config.INPUT_NAMES[index]
        font_curve.font = bpy.data.fonts.load(CURRENT_DIR + "input/blockbit.ttf")
        font_obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)

        bpy.context.scene.collection.objects.link(font_obj)

        font_obj.select_set(True)
        bpy.context.view_layer.objects.active = font_obj

        font_obj.location = (footer_plate.location.x * 2, footer_plate.location.y * 1.2, footer_plate.location.z + 0.1)

        font_obj.dimensions = (footer_plate.dimensions[0] * .7, footer_plate.dimensions[1] * .7, 0.1)

        bpy.ops.object.convert(target='MESH')

        utils.solidify_object(not config.INVERT_QR_CODE, config.BASEPLATE_THICKNESS)

        bpy.ops.object.select_all(action='SELECT')

        # Rotate the whole structure 180 degrees along the z axis.
        # The sd card bottom hole prints better this way because the first ring has time to cool before applying the full layer. 
        bpy.ops.transform.rotate(value=3.14159, orient_axis='Z')


# Select all the QR code objects
'''
for obj in qr_objects:
    obj.select_set(True)


# Set the active object to the first one in the list for the join operation
bpy.context.view_layer.objects.active = qr_objects[0]

# Join all selected objects
bpy.ops.object.join()

# Get a list of all collections
all_collections = list(bpy.data.collections)

# Loop through and delete all other collections
for coll in all_collections[1:]:
    bpy.data.collections.remove(coll)
'''
utils.end(current_time)

# print("Coordinates for QR codes grid:")
# for obj in qr_objects:
    # print(f"Name: {obj.name}, X: {obj.location.x}, Y: {obj.location.y}")
    # utils.debug_object(obj)

'''
def add_string(text, qr_code_obj):

    bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    text_obj = bpy.context.object
    bpy.ops.font.select_all()
    bpy.ops.font.delete(type='SELECTION')
    bpy.ops.font.text_insert(text=text)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    new_location = (
        qr_code_obj.location.x + config.TEXT_X_OFFSET,
        qr_code_obj.location.y + config.TEXT_Y_OFFSET,
        qr_code_obj.location.z + qr_code_obj.dimensions.z + text_obj.dimensions.z/2
    )
    text_obj.location = new_location
    # text_obj.dimensions = (QR_CODE_SIZE, QR_CODE_SIZE, text_obj.dimensions.z)

    # text_obj.data.extrude = 0.1

    # text_obj.data.font = bpy.data.fonts.load(TEXT_FILE_LOCATION)
    text_obj.data.size = config.FONT_SIZE
    
    # 
    text_obj.dimensions.y = 1

    # text_obj.data.space_character = 1.4

    qr_code_obj.users_collection[0].objects.link(text_obj)
    bpy.context.collection.objects.unlink(text_obj)

    return text_obj
'''