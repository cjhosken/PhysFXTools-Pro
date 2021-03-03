import bpy
from bpy.types import Operator
from modules.funcs import show_message_box

class PhysFXToolsPro_OT_GroupCollisions(Operator):
    bl_label = "Group Collisions"    
    bl_idname = "physfxtoolspro.groupcollisions"
    bl_description = "Adds an identical collision modifier to selected objects."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.physfxtoolspro_props
        active_objects = context.selected_objects
        if len(active_objects) > 0:
            for obj in active_objects:
                if (obj.type == 'MESH'):
                    obj.modifiers.new("Group Collision", 'COLLISION')
                    mod = obj.collision
                    mod.use_particle_kill = props.kill_particles
                    mod.damping_factor = props.particle_damping
                    mod.friction_factor = props.particle_friction

                    mod.damping_random = props.particle_random
                    mod.friction_random = props.particle_random

                    mod.damping = props.cloth_damping
                    mod.thickness_outer = props.cloth_thickness
                    mod.cloth_friction = props.cloth_friction
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No objects selected!", "ERROR")
            return {'CANCELLED'}

class PhysFXToolsPro_OT_DeleteCollisions(Operator):
    bl_label = "Delete Collisions"
    bl_idname = "physfxtoolspro.deletecollisions"
    bl_description = "Deletes all collision modifiers from selected objects."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        active_objects = context.selected_objects
        if len(active_objects) > 0:
            for obj in active_objects:
                if obj.type == "MESH":
                    for mod in obj.modifiers:
                        if mod.type == "COLLISION":
                            obj.modifiers.remove(mod) 
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No objects selected!", "ERROR")
            return {'CANCELLED'}

class PhysFXToolsPro_OT_GroupRigidBodies(Operator):
    bl_label = "Group Rigid Bodies"    
    bl_idname = "physfxtoolspro.grouprigidbodies"
    bl_description = "Adds an identical rigid body property to selected objects."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.physfxtoolspro_props
        active_objects = context.selected_objects
        if len(active_objects) > 0:
            main_obj = active_objects[0]

            if main_obj.type == 'MESH':
                bpy.ops.rigidbody.object_add()
                if main_obj.rigid_body is not None:
                    if props.rigidbody_is_active:
                        main_obj.rigid_body.mass = props.rigidbody_mass
                    main_obj.rigid_body.collision_shape = props.rigidbody_shape
                    main_obj.rigid_body.mesh_source = props.rigidbody_source
                    main_obj.rigid_body.friction = props.rigidbody_friction
                    main_obj.rigid_body.restitution = props.rigidbody_bounce
                    main_obj.rigid_body.use_margin = True
                    main_obj.rigid_body.collision_margin = props.rigidbody_margin
                else:
                    show_message_box("Uh oh!", "Something went wrong.", "ERROR")
                    return {'CANCELLED'}

                bpy.ops.rigidbody.object_settings_copy()
                return {'FINISHED'}
            else:
                show_message_box("Uh oh!", "Please select a mesh!", "ERROR")
                return {'CANCELLED'}
        else:
            show_message_box("Uh oh!", "No objects selected!", "ERROR")
            return {'CANCELLED'}

class PhysFXToolsPro_OT_DeleteRigidBodies(Operator):
    bl_label = "Delete Rigid Bodies"
    bl_idname = "physfxtoolspro.deleterigidbodies"
    bl_description = "Deletes all rigid body properties from selected objects."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        active_objects = context.selected_objects
        if len(active_objects) > 0:
            bpy.ops.rigidbody.objects_remove()
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No objects selected!", "ERROR")
            return {'CANCELLED'}
