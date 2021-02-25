import bpy
from bpy.types import Operator

def arrdiff(x, y):
    return (x - y).normalized()

def show_message_box(title="Message Box", message="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class PhysFXTools_OT_Glue(Operator):
    bl_label = 'Glue'
    bl_idname = 'physfxtools.gluebodies'
    bl_description = 'Glues rigid bodies together.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        rigidbodyworld = context.scene.rigidbody_world
        depsgraph = context.evaluated_depsgraph_get()
        active_collection = context.collection
        glue_collection_name = active_collection.name + '_glue'

        if (active_collection.name == "Master Collection"):
            show_message_box("No Collection Selected!",
                             "Please select a collection to glue.", 'ERROR')
            return({'CANCELLED'})

        if (rigidbodyworld is None or not rigidbodyworld.enabled):
            show_message_box("No Rigid Body World!",
                             "Please create a rigid body world.", 'ERROR')
            return({'CANCELLED'})

        else:
            glue_collection = bpy.data.collections.get(glue_collection_name)
            if glue_collection is not None:
                for obj in glue_collection.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
            else:
                glue_collection = bpy.data.collections.new(glue_collection_name)

            for idx, current_obj in enumerate(active_collection.objects):
                if current_obj.type == "MESH":
                    current_obj_mesh = depsgraph.objects.get(current_obj.name, None)
                    if current_obj_mesh is not None:
                        for __, next_obj in enumerate(active_collection.objects[idx+1:]):
                            if next_obj.type == "MESH":
                                next_obj_mesh = depsgraph.objects.get(next_obj.name, None)
                                if next_obj_mesh is not None:
                                    try:
                                        is_current_obj_intersection, current_obj_intersection_point = current_obj.ray_cast(current_obj.location - current_obj.location,
                                                arrdiff(next_obj.location, current_obj.location), distance=1000000,
                                                depsgraph=depsgraph)[:2]
                                        is_next_obj_intersection, next_obj_intersection_point = next_obj.ray_cast(next_obj.location - next_obj.location,
                                                arrdiff(current_obj.location, next_obj.location), distance=1000000,
                                                depsgraph=depsgraph)[:2]
                                    except RuntimeError:
                                        show_message_box("Uh oh!","A runtime error occured.", 'ERROR')
                                        return {'CANCELLED'}
                                    
                                    current_obj_intersection_point += next_obj.location
                                    next_obj_intersection_point += current_obj.location

                                    if not (is_current_obj_intersection and is_next_obj_intersection):
                                        print("UH OH")
                                        continue
                                    
                                    if (current_obj_intersection_point - next_obj_intersection_point).length_squared <= context.scene.physfxtools_settings.glue_distance:
                                        print("WEEEE")
                                        constraint_name = f"Glue_[{current_obj.name}-{next_obj.name}]"
                                        constraint_obj = bpy.data.objects.new(constraint_name, object_data=None)
                                        constraint_obj.location = current_obj_intersection_point
                                        context.scene.collection.objects.link(constraint_obj)
                                        context.view_layer.objects.active = constraint_obj
                                        bpy.ops.rigidbody.constraint_add()
                                        glue_collection.objects.link(constraint_obj)
                                        context.scene.collection.objects.unlink(constraint_obj)
                                        constraint = constraint_obj.rigid_body_constraint
                                        constraint.type = 'FIXED'
                                        constraint.object1 = current_obj
                                        constraint.object2 = next_obj
                                        constraint.use_breaking = context.scene.physfxtools_settings.is_breakable
                                        constraint.breaking_threshold = context.scene.physfxtools_settings.breaking_threshold

            if glue_collection_name not in active_collection.children:
                active_collection.children.link(glue_collection)
            return {'FINISHED'}

#############################################################


class PhysFXTools_OT_DeleteGlue(Operator):
    bl_label = 'Delete Glue'
    bl_idname = 'physfxtools.deleteglue'
    bl_description = 'Deletes Glue'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_collection = context.collection
        if active_collection.name.endswith("_glue"):
            child_collections = bpy.data.collections.get(active_collection.name)
            for obj in child_collections.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(child_collections)
            return{'FINISHED'}
        else:
            show_message_box("Please select a constraint collection to delete.",
                             "No Constraint Collection Selected!", 'ERROR')
            return{'CANCELLED'}

###########################################################


class PhysFXTools_OT_ProxyMesh(Operator):
    bl_label = "Proxy Mesh"
    bl_idname = "physfxtools.proxymesh"
    bl_description = "Creates a proxy mesh around a target object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        base_mesh = context.active_object

        if (base_mesh is None or base_mesh.type != 'MESH'):
            show_message_box("Please select an object to proxy.", "No Object Selected!", 'ERROR')
            return {'CANCELLED'}
        else:
            resize = [0, 0, 0]

            for i in range(0, 3):
                resize[i] = base_mesh.dimensions[i] * base_mesh.scale[i]

            # CREATES A CUBE
            bpy.ops.mesh.primitive_cube_add(size=2, calc_uvs=True,enter_editmode=False, align='WORLD', location=base_mesh.location, rotation=base_mesh.rotation_euler)

            proxy_mesh = context.object
            

            # SCALES AND SUBDIVIDES THE CUBE
            proxy_mesh.name = base_mesh.name + '_proxy'
            proxy_mesh.scale = resize
            modifier = proxy_mesh.modifiers.new('Subdivsion', 'SUBSURF')
            modifier.subdivision_type = 'SIMPLE'
            modifier.levels = 6

            # SHRINKWRAPS THE CUBE
            modifier = proxy_mesh.modifiers.new('Shrinkwrap', 'SHRINKWRAP')
            modifier.offset = context.scene.physfxtools_settings.proxy_distance
            modifier.target = base_mesh

            # REMESHES THE CUBE
            modifier = proxy_mesh.modifiers.new('Remesh', 'REMESH')
            modifier.mode = 'SMOOTH'
            modifier.octree_depth = context.scene.physfxtools_settings.proxy_resolution
            modifier.use_smooth_shade = True

            proxy_mesh.select_set(True)
            bpy.ops.object.convert(target='MESH', keep_original=False)

            # Parents the Proxy to the base mesh
            proxy_mesh.parent = base_mesh
            proxy_mesh.matrix_parent_inverse = base_mesh.matrix_world.inverted()
            return{'FINISHED'}

###########################################################

class PhysFXTools_OT_GroupCollisions(Operator):
    bl_label = "Group Collisions"    
    bl_idname = "physfxtools.groupcollisions"
    bl_description = "Adds the collision property to selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) > 0:
            for obj in objs:    
                if (obj.type == 'MESH'):
                    obj.modifiers.new(type='COLLISION', name="Collision")
                    obj.collision.friction_factor = context.scene.physfxtools_settings.collision_friction
                    obj.collision.damping_factor = context.scene.physfxtools_settings.collision_damping
            return {'FINISHED'}
        else:
            show_message_box("Please select objects to add collision to.","No Objects Selected!", 'ERROR')  
            return{'CANCELLED'}

###########################################################

class PhysFXTools_OT_DeleteGroupCollisions(Operator):
    bl_label = "Delete Group Collisions"
    bl_idname = "physfxtools.deletegroupcollisions"
    bl_description = "Deletes the collision propety from selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) > 0:
            for obj in objs:
                if obj.type == 'MESH':
                    for mod in obj.modifiers:
                        if(mod.type == "COLLISION"):
                            obj.modifiers.remove(mod)
            return {'FINISHED'}                   
        else:
            show_message_box("Please select aobject to add collisions to.","No Object Selected!", 'ERROR')
            return {'CANCELLED'}