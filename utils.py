import bpy
import datetime
import mathutils
from config import *

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

def dimension_check():
    scene = bpy.context.scene
    print("Unit Scale:", setattr(scene.unit_settings, 'scale_length', SCALE) or scene.unit_settings.scale_length)
    print("Length Unit:", setattr(scene.unit_settings, 'length_unit', SCENE_UNITS) or scene.unit_settings.length_unit)
    print("Unit System:", setattr(scene.unit_settings, 'system', SCENE_SYSTEM) or scene.unit_settings.system, "\n")

def debug_object(obj):
    print(f"    Name: {obj.name}")
    for collection in obj.users_collection:
        print(f"    In collection: {collection.name}")
    print(f"    Scale Factor (x,y,z): ({round(obj.scale.x, 2)}, {round(obj.scale.y, 2)}, {round(obj.scale.z, 2)})")
    print(f"    Dimensions (x,y,z): ({', '.join([f'{dimension:.2f}' for dimension in obj.dimensions])}) {SCENE_UNITS}")
    print("\n")
   
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

def solidify_object(invert_code):
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = QR_CODE_THICKNESS 

    if invert_code:
        bpy.context.object.modifiers["Solidify"].offset = 1
    
    bpy.ops.object.modifier_apply(modifier="Solidify")

def center_object(obj):
    center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
    for vertex in obj.data.vertices:
        vertex.co -= center_of_mass
        
    center_of_mass = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(obj.data.vertices)
    for vertex in obj.data.vertices:
        vertex.co -= center_of_mass

    return bpy.context.view_layer.objects.active

def duplicate_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0)})
    
    # Get the newly duplicated object and deselect original object
    duplicated_obj = bpy.context.view_layer.objects.active
    obj.select_set(False)
    
    return duplicated_obj

def set_origin_to_center(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='BOUNDS')


def end(current_time):
    bpy.ops.export_mesh.stl(filepath="C:\\Users\\qfran\\Desktop\\Blender\\code\\qr_code\\output\\file.stl")

    # Calculate the elapsed time in milliseconds
    elapsed_time = round((datetime.datetime.now() - current_time).total_seconds(), 2)
    print("\n======================================================")
    print("Run Time:", elapsed_time, "seconds")
    print("======================================================\n")

    #print(f"Memory used during script execution: {memory_used} bytes")
  