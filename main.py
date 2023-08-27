import bpy
import mathutils
import datetime
import bmesh
import numpy as np
from scipy.spatial import ConvexHull
import math
import os
import time

SCALE = 1
SCENE_SYSTEM = 'METRIC'
SCENE_UNITS = 'MILLIMETERS'

QR_CODE_SIZE = 20
QR_SPACING = 0
QR_CODE_THICKNESS = .2
QUIET_ZONE = 8

BASEPLATE_THICKNESS = .2

TEXT_FILE_LOCATION = 'C:\\Users\\qfran\\Desktop\\Blender\\code\\qr_code\\blockbit.ttf'

GRID_SIZE = 2

# Have to adjust these based on text. A real sicko would figure out how to automate this. 
FONT_SIZE = 6
TEXT_X_OFFSET = 4
TEXT_Y_OFFSET = -1

# If the bottom layer is transparent, then invert the code so you can put a sticker as the back
INVERT_QR_CODE = True

def start():
    # Clear the console
    from os import system; 
    cls = lambda: system('cls'); 
    cls()

    # Get the current date and time
    current_time = datetime.datetime.now()

    print("\n======================================================")
    print("Current Date and Time:", current_time)
    print("======================================================")

    dimension_check()
    clear_scene()

    return current_time

def end(current_time):
    bpy.ops.export_mesh.stl(filepath="C:\\Users\\qfran\\Desktop\\Blender\\code\\qr_code\\output\\file.stl")

    # Calculate the elapsed time in milliseconds
    elapsed_time = round((datetime.datetime.now() - current_time).total_seconds(), 2)
    print("\n======================================================")
    print("Run Time:", elapsed_time, "seconds")
    print("======================================================\n")

    #print(f"Memory used during script execution: {memory_used} bytes")
    
def dimension_check():
    scene = bpy.context.scene
    print("Unit Scale:", setattr(scene.unit_settings, 'scale_length', SCALE) or scene.unit_settings.scale_length)
    print("Length Unit:", setattr(scene.unit_settings, 'length_unit', SCENE_UNITS) or scene.unit_settings.length_unit)
    print("Unit System:", setattr(scene.unit_settings, 'system', SCENE_SYSTEM) or scene.unit_settings.system, "\n")

def clear_scene():
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    # Delete objects
    objects_to_delete = list(bpy.data.objects)
    for obj in objects_to_delete:
        #print('Deleting object:',obj.name)
        bpy.data.objects.remove(obj)

    # Delete collections
    for collection in bpy.data.collections:
        #print('Deleting collection:',collection.name)
        bpy.data.collections.remove(collection)

def merge_objects(collection):
    # Convert all objects in the collection to meshes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')

    # Join all converted mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = collection.objects[0]
    bpy.ops.object.join()

    return bpy.context.view_layer.objects.active

def import_image(svg_file_path):

    # Get a set of current collections before importing
    current_collections = set(bpy.data.collections.keys())

    # Import the SVG file
    bpy.ops.import_curve.svg(filepath=svg_file_path)

    # Find the newly added collection
    new_collections = set(bpy.data.collections.keys()) - current_collections
    if not new_collections:
        raise ValueError(f"Failed to import and find a new collection from SVG at {svg_file_path}")
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
    scale_factor = QR_CODE_SIZE / max(bpy.context.view_layer.objects.active.dimensions)
    bpy.context.view_layer.objects.active.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Return the joined curve object
    return bpy.context.view_layer.objects.active

def debug_object(obj):
    print(f"    Name: {obj.name}")
    for collection in obj.users_collection:
        print(f"    In collection: {collection.name}")
    print(f"    Scale Factor (x,y,z): ({round(obj.scale.x, 2)}, {round(obj.scale.y, 2)}, {round(obj.scale.z, 2)})")
    print(f"    Dimensions (x,y,z): ({', '.join([f'{dimension:.2f}' for dimension in obj.dimensions])}) {SCENE_UNITS}")
        
def add_timestamp(text, qr_code_obj):

    bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    text_obj = bpy.context.object
    bpy.ops.font.select_all()
    bpy.ops.font.delete(type='SELECTION')
    bpy.ops.font.text_insert(text=text)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    new_location = (
        qr_code_obj.location.x + TEXT_X_OFFSET,
        qr_code_obj.location.y + TEXT_Y_OFFSET,
        qr_code_obj.location.z + qr_code_obj.dimensions.z + text_obj.dimensions.z/2
    )
    text_obj.location = new_location
    # text_obj.dimensions = (QR_CODE_SIZE, QR_CODE_SIZE, text_obj.dimensions.z)

    # text_obj.data.extrude = 0.1

    # text_obj.data.font = bpy.data.fonts.load(TEXT_FILE_LOCATION)
    text_obj.data.size = FONT_SIZE
    
    # 
    text_obj.dimensions.y = 1

    # text_obj.data.space_character = 1.4

    qr_code_obj.users_collection[0].objects.link(text_obj)
    bpy.context.collection.objects.unlink(text_obj)

    return text_obj

def add_baseplate(obj):

    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.active_object.dimensions = (obj.dimensions.x + QUIET_ZONE, obj.dimensions.y + QUIET_ZONE, 1)
    obj.users_collection[0].objects.link(bpy.context.active_object)
    bpy.context.collection.objects.unlink(bpy.context.active_object)
    solidify_object(True)

    return bpy.context.active_object

def apply_grid(obj):
    
    if(GRID_SIZE > 1):
        # Get the dimensions of the object
        dimensions = obj.dimensions

        # Duplicate the object in a grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i == 0 and j == 0:  # The original object, no need to duplicate
                    continue
                # Duplicate the object
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                new_obj.animation_data_clear()
                
                # Update the location of the new object
                new_obj.location.x += i * dimensions.x
                new_obj.location.y += j * dimensions.y
                
                # Link the new object to the scene
                bpy.context.collection.objects.link(new_obj)
                
        # Select all objects
        bpy.ops.object.select_all(action='SELECT')

        # Get the active object
        active_obj = bpy.context.active_object

        # Join all selected objects (this will join them into the active object)
        bpy.ops.object.join()
        
def position_in_grid(obj, i, j):
    """Position the object at the (i, j) index of the grid."""
    # Calculate the offset based on the dimensions of the object
    offset_x = i * (obj.dimensions.x + QR_SPACING)
    offset_y = j * (obj.dimensions.y + QR_SPACING)

    # Update the location of the object
    obj.location.x += offset_x
    obj.location.y += offset_y

def center_object(obj):
    center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
    for vertex in obj.data.vertices:
        vertex.co -= center_of_mass
        
    center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
    for vertex in obj.data.vertices:
        vertex.co -= center_of_mass

    return bpy.context.view_layer.objects.active

def solidify_object(invert_code):
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = QR_CODE_THICKNESS 

    if invert_code:
        bpy.context.object.modifiers["Solidify"].offset = 1
    
    bpy.ops.object.modifier_apply(modifier="Solidify")

def main():
    current_time = start()
    
    input_dir = "C:\\Users\\qfran\\Desktop\\Blender\\code\\qr_code\\input\\"

    # Filter out only the SVG files
    svg_files = [f for f in os.listdir(input_dir) if f.endswith(".svg")]
    total_files = len(svg_files)
    
    # Calculate the grid size
    GRID_SIZE = int(total_files**0.5) + (1 if (total_files**0.5) % 1 > 0 else 0)  # Ceiling of the square root

    # List to store all the QR code objects
    qr_objects = []

    date = datetime.date.today()

    current_date = date.strftime('%Y-%m-%d')

    input_names = [
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1",
        "SL-1"
    ];

    for index, filename in enumerate(svg_files):

        svg_file_path = os.path.join(input_dir, filename)
        image_obj = import_image(svg_file_path)

        collection = image_obj.users_collection[0]
        input_string = input_names[index]
        add_timestamp(input_string, image_obj)

        merged_object = center_object(merge_objects(collection))
        solidify_object(False)
        add_baseplate(image_obj)

        merged_object = center_object(merge_objects(collection))
        # cut_qr_code(merged_object)
        bpy.context.view_layer.objects.active = merged_object
        bpy.ops.transform.rotate(value=3.14159, orient_axis='Y')

        # Calculate position in the grid
        i = index // GRID_SIZE  # integer division gives the row number
        j = index % GRID_SIZE   # modulo gives the column number

        position_in_grid(image_obj, i, j)

        qr_objects.append(merged_object)

    # Select all the QR code objects
    for obj in qr_objects:
        obj.select_set(True)

    '''
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
    end(current_time)

main()