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
        active_objects = []

        if len(context.selected_objects) > 0:
            for obj in context.selected_objects:
                active_objects.append(obj)

            for obj in active_objects:
                if (obj.type == "MESH"):
                    resize_scale = obj.dimensions / 2.0
                    bpy.ops.mesh.primitive_cube_add()
                    proxy_mesh = context.object
                    proxy_mesh.name = obj.name + "_proxy"
                    proxy_mesh.scale = resize_scale
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

                    proxy_mesh.parent = obj
                    proxy_mesh.matrix_parent_inverse = obj.matrix_world.inverted()

                    bpy.ops.object.convert(target='MESH', keep_original=False)
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No objects selected!", "ERROR")
            return {'CANCELLED'}

class PhysFXToolsPro_OT_DeleteProxyMesh(Operator):
    bl_label = "Delete Proxy Mesh"
    bl_idname = "physfxtoolspro.deleteproxymesh"
    bl_description = "Deletes all proxy meshes inside the active collection."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _collection = context.collection
        self.traverse(_collection)
        return {'FINISHED'}

    def traverse(self, _collection):
        if len(_collection.children) > 0:
            for col in _collection.children:
                self.traverse(col)
        else:
            for obj in _collection.objects:
                if obj.name.endswith("_proxy"):
                    bpy.data.objects.remove(obj, do_unlink=True)
        return {'FINISHED'}