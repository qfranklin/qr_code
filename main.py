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

def add_baseplate(obj):

    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.dimensions = (obj.dimensions.x + config.QUIET_ZONE, obj.dimensions.y + config.QUIET_ZONE, 1)
    obj.users_collection[0].objects.link(bpy.context.active_object)
    bpy.context.collection.objects.unlink(bpy.context.active_object)
    utils.solidify_object(True)

    return bpy.context.active_object
     
def position_in_grid(obj, i, j):

    # print(f"    {i} {j} i j")

    offset_y = i * (obj.dimensions.y + config.QR_SPACING)
    offset_x = j * (obj.dimensions.x + config.QR_SPACING)
    obj.location.x += offset_x
    obj.location.y += offset_y

def create_qr_code(index):
    
    print("create_qr start")

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # Adjust version as needed
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    print("INDEX: ", index)

    # Add the data to the QR code
    qr.add_data(config.INPUT_QR_STRINGS[index])
    qr.make(fit=True)

    # Create an SVG image factory
    factory = qrcode.image.svg.SvgPathImage

    # Generate the SVG QR code
    svg_image = qr.make_image(image_factory=factory)

    # CURRENT_DIR + "input\\"
    # print("current directory: " + os.getcwd())
    # print("saved file name: " + file_input_path)

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

    qr_code = bpy.context.view_layer.objects.active

    collection = qr_code.users_collection[0]

    '''
    if(config.REPEAT):
        input_string = config.INPUT_NAMES[0]
    else:
        input_string = config.INPUT_NAMES[index]
    
    add_string(input_string, qr_code)
    '''

    merged_object = utils.center_object(utils.merge_objects(collection))
    utils.solidify_object(False)
    add_baseplate(qr_code)

    merged_object = utils.center_object(utils.merge_objects(collection))
    bpy.context.view_layer.objects.active = merged_object
    bpy.ops.transform.rotate(value=3.14159, orient_axis='Y')

    return qr_code

def main():

    current_time = utils.start()

    '''
    if config.REPEAT:
        for index in range(config.REPEAT):
            qr_objects.append((index, config.REPEAT_FILENAME))
    else:
        # Filter out only the SVG files
        svg_files = [f for f in os.listdir(CURRENT_DIR + "input\\") if f.endswith(".svg")]
        for index, svg_file in enumerate(svg_files):
            qr_objects.append((index, svg_file))
    '''

    # Calculate the grid size
    grid_size = int(len(config.INPUT_QR_STRINGS)**0.5) + (1 if (len(config.INPUT_QR_STRINGS)**0.5) % 1 > 0 else 0)  # Ceiling of the square root

    # Import image once before loop if REPEAT is set
    image_obj = None
    if config.REPEAT:
        print("REPEAT!!!!!!!!!!!!!")
        image_obj = create_qr_code(0)
        utils.set_origin_to_center(image_obj)
        image_obj.location = (0, 0, 0)

    for index, input_string in enumerate(config.INPUT_QR_STRINGS):

        # print(f"{index} start loop {len(qr_objects)}")

        # print(f"Dimensions for QR code {index}: {image_obj.dimensions}")

        # Import image inside loop only if REPEAT is not set
        image_obj = create_qr_code(index)

        '''
        if not config.REPEAT:
            image_obj = create_qr_code(index)
        else: 
            image_obj = utils.duplicate_object(image_obj)
            utils.set_origin_to_center(image_obj)
        '''

        # utils.debug_object(image_obj)

        image_obj.location = (0, 0, 0)

        # Calculate position in the grid
        i = index // grid_size  # integer division gives the row number
        j = index % grid_size   # modulo gives the column number

        position_in_grid(image_obj, i, j)

        # utils.debug_object(image_obj)
        # print(f"Name: {image_obj.name}, X: {image_obj.location.x}, Y: {image_obj.location.y}, Width: {image_obj.dimensions.x}, Height: {image_obj.dimensions.y}")
        print(f"Width: {image_obj.dimensions.x}")
        print(f"Height: {image_obj.dimensions.y}")

        # qr_objects.append(merged_object)

        # print(f"{index} end loop")

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

main()