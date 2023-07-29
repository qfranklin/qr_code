import bpy
import mathutils
import datetime
import bmesh
import numpy as np
from scipy.spatial import ConvexHull
import math

# TODO figure out why the python instance needs to import the current project
import sys
sys.path.append(r"C:\Users\qfran\Desktop\Blender\code\qr_code")
from setup import clear_console

SCALE = 1
SIZE = 35
SCENE_SYSTEM = 'METRIC'
SCENE_UNITS = 'MILLIMETERS'
QR_CODE_THICKNESS = .5
SVG_FILE_PATHS = 'C:\\Users\\qfran\\Desktop\\gimp\\qrcode_script.svg'
GRID_SIZE = 1

clear_console()

def merge_objects_in_collection(collection):
    # Merge objects in the given collection
    objects_to_merge = [obj for obj in collection.objects if obj.type == 'MESH']
    if len(objects_to_merge) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects_to_merge:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objects_to_merge[0]
        bpy.ops.object.join()

def __post_image_import():
    
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
    collection_name = "qrcode_script.svg" # specify your collection name here
    collection = bpy.data.collections[collection_name]
    for obj in collection.objects:
        if obj.type == 'CURVE':
            obj.select_set(True)
        else:
            obj.select_set(False)

    # Set active object to be the first selected curve to allow 'join' operator
    bpy.context.view_layer.objects.active = next(obj for obj in collection.objects if obj.select_get())

    # Join selected curves
    bpy.ops.object.join()
    
    
def __merge_mesh(collection_name):
    
    collection = bpy.data.collections[collection_name]
    mesh_objs = [obj for obj in collection.objects if obj.type == 'MESH']

    if not mesh_objs:
        raise ValueError("No mesh objects found in collection")

    # Get all vertices of all mesh objects in collection
    all_verts = np.array([
        vert.co for obj in mesh_objs
        for vert in obj.data.vertices
    ])

    # Calculate convex hull
    hull = ConvexHull(all_verts)

    # Create new mesh and link it to scene
    mesh = bpy.data.meshes.new("Hull")
    obj = bpy.data.objects.new("Hull", mesh)
    bpy.context.collection.objects.link(obj)

    # Create bmesh object and add vertices and faces
    bm = bmesh.new()
    for vertex in hull.points:
        bm.verts.new(vertex)

    bm.verts.ensure_lookup_table()

    for simplex in hull.simplices:
        try:
            bm.faces.new([bm.verts[i] for i in simplex])
        except ValueError:
            # If face already exists, ignore
            pass

    # Update bmesh to mesh
    bm.to_mesh(mesh)
    bm.free()
    
def debug_object(obj):
    
    print(f"    Name: {obj.name}")
    
    # Loop over the collections to which the object belongs and print their names
    for collection in obj.users_collection:
        
        # no object should be in the Scene Collection. Added because dont know 
        if(collection.name == 'Scene Collection'):
            collection.objects.unlink(obj)
            continue
        
        print(f"    In collection: {collection.name}")
        
    # Print the scale factors
    print(f"    Scale Factor (x,y,z): ({round(obj.scale.x, 2)}, {round(obj.scale.y, 2)}, {round(obj.scale.z, 2)})")

    # Get the dimensions of the object in Blender units
    labels = ["Width (X)", "Depth (Y)", "Height (Z)"]
    print(f"    Dimensions (x,y,z): ({', '.join([f'{dimension:.2f}' for dimension in obj.dimensions])}) {SCENE_UNITS}")
        
def main():
    # Get the current date and time
    current_time = datetime.datetime.now()

    print("\n======================================================")
    print("Current Date and Time:", current_time)
    print("======================================================")

    # Get the active scene
    scene = bpy.context.scene

    # Update the scene's unit settings and print the updated unit settings
    print("Unit Scale:", setattr(scene.unit_settings, 'scale_length', SCALE) or scene.unit_settings.scale_length)
    print("Length Unit:", setattr(scene.unit_settings, 'length_unit', SCENE_UNITS) or scene.unit_settings.length_unit)
    print("Unit System:", setattr(scene.unit_settings, 'system', SCENE_SYSTEM) or scene.unit_settings.system, "\n")

    # We will be switching between object and edit mode frequently
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    # Let's clear the scene by deleting everything

    # Delete objects
    objects_to_delete = list(bpy.data.objects)
    for obj in objects_to_delete:
        #print('Deleting object:',obj.name)
        bpy.data.objects.remove(obj)

    # Delete collections
    for collection in bpy.data.collections:
        #print('Deleting collection:',collection.name)
        bpy.data.collections.remove(collection)

    # Import the image, it is now alive
    bpy.ops.import_curve.svg(filepath=SVG_FILE_PATHS)


    __post_image_import()

    mesh_objects = []

    for index, obj in enumerate(bpy.data.objects):
        
        collection = obj.users_collection[index]
        collection.name = "QR_CODE_"+str(index)
    
        # convert to mesh
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.convert(target='MESH')
        obj.select_set(False)
        
        # Add to mesh_objects
        mesh_objects.append(obj)
            
        print("Select: "+obj.name)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        print("  Centering")
        center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
        for vertex in obj.data.vertices:
            vertex.co -= center_of_mass
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        
        print("  Resizing")
        current_dimensions = obj.dimensions
        max_dimension = max(current_dimensions)
        # Calculate the scale factor to achieve the desired size
        scale_factor = SIZE / max_dimension
        print(f"{scale_factor} {SIZE} {max_dimension}")
        obj.scale = (scale_factor, scale_factor, scale_factor)
        
        # Ensure the object is selected and is the active object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)  # Apply scale here

        print("  Solidify")
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = QR_CODE_THICKNESS 
        bpy.ops.object.modifier_apply(modifier="Solidify")
        
        print("  Add Baseplate")
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
        
        baseplate_obj = bpy.context.active_object
        
        # Set baseplate dimensions based on QR code
        baseplate_obj.dimensions = (obj.dimensions.x + 2, obj.dimensions.y + 2, 1)
        collection.objects.link(baseplate_obj)
        
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = QR_CODE_THICKNESS
        bpy.context.object.modifiers["Solidify"].offset = QR_CODE_THICKNESS 
        bpy.ops.object.modifier_apply(modifier="Solidify")
        
        # Apply the scale transformation to the cutter
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Select all meshes in the collection
        for obj in collection.objects:
            if obj.type == 'MESH':
                obj.select_set(True)

        # Ensure there's something to join
        if bpy.context.selected_objects:
            # Set active object to be the first selected mesh to allow 'join' operator
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
            # Join selected meshes
            bpy.ops.object.join()
            # Rename the joined object
            bpy.context.active_object.name = collection.name + '_merged'

        # add cuts 
        """
        
        # Set mode to Object
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the current active object
        obj = bpy.context.active_object

        # Get mesh data from the object
        mesh = obj.data

        # Create a BMesh instance
        bm = bmesh.new()

        # Load the mesh data into the BMesh instance
        bm.from_mesh(mesh)

        # Set all faces to unselected
        for f in bm.faces:
            f.select = False

        # Initialize a variable to keep track of the highest face
        highest_face = None
        highest_z = -float("inf")

        # Loop through each face
        for f in bm.faces:
            # Get the average z-coordinate of the face
            face_z = sum([v.co.z for v in f.verts])/len(f.verts)
            
            # If this face is higher than the current highest, update our tracking variables
            if face_z > highest_z:
                highest_z = face_z
                highest_face = f

        # Set the highest face to selected
        if highest_face is not None:
            highest_face.select = True

        # Update the mesh data with the new selection
        bm.to_mesh(mesh)
        bm.free()

        # Set mode to Edit
        bpy.ops.object.mode_set(mode='EDIT')

        # Apply the bevel
        bpy.ops.mesh.bevel(offset_type='OFFSET', offset=0.5)  # Adjust the offset parameter as needed

        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        """



    # Get the active object
    obj = bpy.context.active_object

    # Set the origin of the object to its geometry
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')












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





    # Make sure the desired mesh object is selected/active
    obj = bpy.context.active_object

    # Switch to Edit Mode (if in Object Mode)
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices, edges, or faces (depending on what you want to rotate)
    bpy.ops.mesh.select_all(action='SELECT')

    # Calculate the 180-degree rotation in radians
    angle_x = math.radians(180)
    angle_y = math.radians(180)

    # Rotate along the X or Y axis
    bpy.ops.transform.rotate(value=angle_x, orient_axis='X')
    # bpy.ops.transform.rotate(value=angle_y, orient_axis='Y')





    # Calculate the height of the object along the Z-axis
    z_coordinates = [v.co.z for v in obj.data.vertices]
    min_z = min(z_coordinates)
    max_z = max(z_coordinates)
    object_height = max_z - min_z

    # Calculate the amount to raise the object to keep it above the clipping boundary
    desired_min_z = 0.0  # Adjust this value as needed based on where you want the object to be positioned
    amount_to_raise = desired_min_z - min_z

    # Move the object along the Z-axis to keep it above the clipping boundary
    obj.location.z += amount_to_raise + .3






    # Switch back to Object Mode to see the result
    bpy.ops.object.mode_set(mode='OBJECT')




    # Calculate the elapsed time in milliseconds
    elapsed_time = round((datetime.datetime.now() - current_time).total_seconds(), 2)
    print("\n======================================================")
    print("Run Time:", elapsed_time, "seconds")
    print("======================================================\n")

    pass

main()

if __name__ == "__main__":
    main()