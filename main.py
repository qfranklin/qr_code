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

    # Save the SVG QR code to a file
    with open(CURRENT_DIR + "input/qrcode.svg", "wb") as f:
        svg_image.save(f)

    print("saved svg")

    # Get a set of current collections before importing
    current_collections = set(bpy.data.collections.keys())

    bpy.ops.import_curve.svg(filepath=CURRENT_DIR + "input\\qrcode.svg")

    # Find the newly added collection
    new_collections = set(bpy.data.collections.keys()) - current_collections
    if not new_collections:
        raise ValueError("Failed to import and find a new collection from SVG")
    collection = bpy.data.collections[new_collections.pop()]

    # Delete the "Curve" object if present
    curve_to_delete = bpy.data.objects.get("Curve")
    if curve_to_delete:
        bpy.ops.object.select_all(action='DESELECT')
        curve_to_delete.select_set(True)
        bpy.ops.object.delete()

    # Set the 3D cursor to the origin
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    # Select curves within the new collection
    for obj in collection.objects:
        if obj.type == 'CURVE':
            obj.select_set(True)
        else:
            obj.select_set(False)

    # Set active object to be the first selected curve to allow 'join' operator
    bpy.context.view_layer.objects.active = next(obj for obj in collection.objects if obj.select_get())

    # Join selected curves
    bpy.ops.object.join()
    bpy.ops.object.convert(target='MESH')

    # Calculate and apply scale factor
    scale_factor = config.QR_CODE_SIZE / max(bpy.context.view_layer.objects.active.dimensions)
    bpy.context.view_layer.objects.active.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    print("create_qr end")

    image_obj = bpy.context.view_layer.objects.active

    collection = image_obj.users_collection[0]

    merged_object = utils.center_object(utils.merge_objects(collection))
    utils.solidify_object(False)

    # Add baseplate to qr code
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.dimensions = (image_obj.dimensions.x + config.QUIET_ZONE, image_obj.dimensions.y + config.QUIET_ZONE, 1)
    image_obj.users_collection[0].objects.link(bpy.context.active_object)
    bpy.context.collection.objects.unlink(bpy.context.active_object)
    utils.solidify_object(True)

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


    print(f"Width: {image_obj.dimensions.x}")
    print(f"Height: {image_obj.dimensions.y}")

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