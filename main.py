import bpy
import mathutils
import datetime
import bmesh
import numpy as np
from scipy.spatial import ConvexHull
import math

#import psutil

# TODO figure out how to use the VSCode Blender extension with a traditional python project
# import sys
# sys.path.append(r"path_to_this_project")
# import setup

SCALE = 1
SIZE = 35
SCENE_SYSTEM = 'METRIC'
SCENE_UNITS = 'MILLIMETERS'
QR_CODE_THICKNESS = .3
BASEPLATE_THICKNESS = .2
QUIET_ZONE = 8
FILE_NAME = 'qrcode_script.svg'
SVG_FILE_PATHS = 'C:\\Users\\qfran\\Desktop\\Blender\\code\\qr_code\\input\\'+FILE_NAME
GRID_SIZE = 1

# If the bottom layer is transparent, then invert the code so you can put a sticker as the back
INVERT_QR_CODE = True

def clear_console():
    # Clear the console
    from os import system; cls = lambda: system('cls'); cls()
    
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

def merge_objects_in_collection(collection):
    # Merge objects in the given collection
    objects_to_merge = [obj for obj in collection.objects if obj.type == 'MESH']
    if len(objects_to_merge) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects_to_merge:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objects_to_merge[0]
        bpy.ops.object.join()

def import_image():

    # Import the image, it is now alive
    bpy.ops.import_curve.svg(filepath=SVG_FILE_PATHS)
    
    # Delete the first curve because it is an inline baseplate. ##can remove at some point and manipulate this curve into the baseplate
    # Step 1: Find and delete the curve with the name "Curve"
    curve_to_delete = bpy.data.objects.get("Curve")
    if curve_to_delete:
        bpy.ops.object.select_all(action='DESELECT')
        curve_to_delete.select_set(True)
        bpy.ops.object.delete()

    # Set the 3D cursor to the origin
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    # Select curves
    collection = bpy.data.collections[FILE_NAME]
    for obj in collection.objects:
        if obj.type == 'CURVE':
            obj.select_set(True)
        else:
            obj.select_set(False)

    # Set active object to be the first selected curve to allow 'join' operator
    bpy.context.view_layer.objects.active = next(obj for obj in collection.objects if obj.select_get())

    # Join selected curves
    bpy.ops.object.join()

def debug_object(obj):
    
    print(f"    Name: {obj.name}")
    
    # Loop over the collections to which the object belongs and print their names
    for collection in obj.users_collection:
        
        # no object should be in the Scene Collection. Added because dont know 
        #if(collection.name == 'Scene Collection'):
        #    collection.objects.unlink(obj)
        #    continue
        
        print(f"    In collection: {collection.name}")
        
    # Print the scale factors
    print(f"    Scale Factor (x,y,z): ({round(obj.scale.x, 2)}, {round(obj.scale.y, 2)}, {round(obj.scale.z, 2)})")

    # Get the dimensions of the object in Blender units
    labels = ["Width (X)", "Depth (Y)", "Height (Z)"]
    print(f"    Dimensions (x,y,z): ({', '.join([f'{dimension:.2f}' for dimension in obj.dimensions])}) {SCENE_UNITS}")
        
def create_timestamp_text(text, qr_code_obj):
    """ Create a 3D text object with given text and location. """
    bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    text_obj = bpy.context.object

    # Clear any default text
    bpy.ops.font.select_all()
    bpy.ops.font.delete(type='SELECTION')
    bpy.ops.font.text_insert(text=text)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Calculate position
    # Get QR Code's bounding box dimensions
    qr_bbox = qr_code_obj.dimensions
    
    # Get text's bounding box dimensions
    text_bbox = text_obj.dimensions

    # Calculate the new position
    # Position the text's bottom-left corner directly above the QR Code's top-left corner
    new_location = (
        qr_code_obj.location.x + 7,
        qr_code_obj.location.y,
        qr_code_obj.location.z + qr_bbox.z + text_bbox.z/2
    )

    text_obj.location = new_location

    return text_obj

def main():

    clear_console()

    # Get the current date and time
    current_time = datetime.datetime.now()

    # Get the current memory usage
    #initial_memory = psutil.virtual_memory().used

    print("\n======================================================")
    print("Current Date and Time:", current_time)
    print("======================================================")

    dimension_check()
    clear_scene()
    import_image()

    for index, obj in enumerate(bpy.data.objects):
        
        collection = obj.users_collection[index]

        # rename collection
        collection.name = "collection_"+str(index)

        # convert curves to mesh
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.convert(target='MESH')

        print("  Scaling")
        current_dimensions = obj.dimensions
        max_dimension = max(current_dimensions)
        # Calculate the scale factor to achieve the desired size
        scale_factor = SIZE / max_dimension
        print(f"  {scale_factor} {SIZE} {max_dimension}")
        obj.scale = (scale_factor, scale_factor, scale_factor)
        # apply the scale
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create 3D timestamp text
        current_dimensions = obj.dimensions
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {timestamp} timestamp")
        text_location = (0, 0, current_dimensions.z)
        text_obj = create_timestamp_text(timestamp, obj)
        text_obj.dimensions = (SIZE, SIZE, text_obj.dimensions.z)
        
        # Adjust font size (change to the desired size)
        font_size = 3.5  # Adjust as needed
        text_obj.data.size = font_size

        # Adjust text box dimensions (width, height)
        new_box_height = 2  # Adjust as needed
        text_obj.dimensions.y = new_box_height

        # Link the text object to the collection
        collection.objects.link(text_obj)
        bpy.context.collection.objects.unlink(text_obj)
        
        # Convert text to mesh
        text_obj.select_set(True)
        bpy.ops.object.convert(target='MESH')
        
        
        obj.select_set(True)
        text_obj.select_set(True)
        
        # Set the active object to the one you want to keep (this will be the main object)
        bpy.context.view_layer.objects.active = obj

        # Join the objects
        bpy.ops.object.join()

        print("  Centering")
        center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
        for vertex in obj.data.vertices:
            vertex.co -= center_of_mass
            
        center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
        for vertex in obj.data.vertices:
            vertex.co -= center_of_mass
            
        print("  Solidify")
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = QR_CODE_THICKNESS 

        if not INVERT_QR_CODE:
            bpy.context.object.modifiers["Solidify"].offset = QR_CODE_THICKNESS 
        
        bpy.ops.object.modifier_apply(modifier="Solidify")

        # Here's where we set the object's origin to its center of mass
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        qr_origin = obj.location.copy()

        print("  Add Baseplate")
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
        baseplate_obj = bpy.context.active_object
        # set baseplate dimensions based on QR code
        baseplate_obj.dimensions = (obj.dimensions.x + QUIET_ZONE, obj.dimensions.y + QUIET_ZONE, 1)
        collection.objects.link(baseplate_obj)
        # This ensures the baseplate is aligned with the QR code/timestamp's origin
        baseplate_obj.location = qr_origin
        # Move the baseplate 3 units along the positive Y-axis
        baseplate_obj.location.y += 3
        # solidify the baseplate
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = BASEPLATE_THICKNESS

        if INVERT_QR_CODE:
            bpy.context.object.modifiers["Solidify"].offset = BASEPLATE_THICKNESS 

        bpy.ops.object.modifier_apply(modifier="Solidify")

        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # select all objects and join them
        for obj in collection.objects:
            if obj.type == 'MESH':
                obj.select_set(True)

        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        # Join selected meshes
        bpy.ops.object.join()
        # Rename the joined object
        bpy.context.active_object.name = 'qr_code'


    # Get the active object
    obj = bpy.context.active_object

    # Set the origin of the object to its geometry
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

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

    '''
    # Make sure the desired mesh object is selected/active
    obj = bpy.context.active_object

    # Calculate the height of the object along the Z-axis
    z_coordinates = [v.co.z for v in obj.data.vertices]
    min_z = min(z_coordinates)
    max_z = max(z_coordinates)
    object_height = max_z - min_z

    # Calculate the amount to raise the object to keep it above the clipping boundary
    desired_min_z = 0.0  # Adjust this value as needed based on where you want the object to be positioned
    amount_to_raise = desired_min_z - min_z

    # Move the object along the Z-axis to keep it above the clipping boundary
    obj.location.z += amount_to_raise + .1

    # Select the object you want to rotate
    obj = bpy.context.active_object

    # Rotate the object around the Y-axis
    obj.rotation_euler[1] += math.pi
    '''

    bpy.ops.export_mesh.stl(filepath="C:\\Users\\qfran\\Desktop\\Blender\\code\\qr_code\\output\\file.stl")

    # Calculate the elapsed time in milliseconds
    elapsed_time = round((datetime.datetime.now() - current_time).total_seconds(), 2)
    print("\n======================================================")
    print("Run Time:", elapsed_time, "seconds")
    print("======================================================\n")

    #print(f"Memory used during script execution: {memory_used} bytes")

main()