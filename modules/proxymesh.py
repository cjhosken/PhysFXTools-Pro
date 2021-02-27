import bpy
import bmesh
from bpy.types import Operator
from modules.funcs import show_message_box

class PhysFXToolsPro_OT_MakeProxyMesh(Operator):
    bl_label = "Proxy Mesh"
    bl_idname = "physfxtoolspro.makeproxymesh"
    bl_description = "Creates a proxy mesh around a target object."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_objects = context.selected_objects

        if len(active_objects) > 0:
            for obj in active_objects:
                if (obj.type == "MESH"):
                    resize_scale = obj.dimensions / 2
                    proxy_mesh = make_cube(obj.name + "_proxy")
                    proxy_mesh.scale(resize_scale)
                    proxy_mesh.location = obj.location
                    proxy_mesh.rotation_euler = obj.rotation_euler

                    tmp_mod = proxy_mesh.modifiers.new("Subdivide_tmp", "SUBSURF")
                    tmp_mod.subdivision_type = 'SIMPLE'
                    tmp_mod.levels = 6

                    tmp_mod = proxy_mesh.modifiers.new('Shrinkwrap_tmp', "SHRINKWRAP")
                    tmp_mod.offset = context.scene.physfxtoolspro_props.proxy_offset
                    tmp_mod.wrap_mode = "ABOVE_SURFACE"
                    tmp_mod.target = obj

                    tmp_mod = proxy_mesh.modifiers.new('Remesh_tmp', "REMESH")
                    tmp_mod.mode = 'SMOOTH'
                    tmp_mod.octree_depth = bpy.context.scene.physfxtoolspro_props.proxy_resolution
                    tmp_mod.use_smooth_shade = True

                    for mod in proxy_mesh.modifiers:
                        bpy.ops.object.modifier_apply(modifier=mod.name)

                    proxy_mesh.parent = obj
                    proxy_mesh.matrix_parent_inverse = obj.matrix_world.inverted()
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No objects selected!", "ERROR")
            return {'CANCELLED'}

def make_cube(name):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.from_edit_mesh(mesh)
    bmesh.ops.create_cube(bm, size=2)
    bm.free()
    return obj