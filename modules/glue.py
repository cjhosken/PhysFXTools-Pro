import bpy
import bmesh
from bpy.types import Operator
from modules.funcs import show_message_box

class PhysFXToolsPro_OT_GlueBodies(Operator): 
    bl_label = "Glue"
    bl_idname = 'physfxtoolspro.gluebodies'
    bl_description = "Glue selected rigidbodies together."
    bl_options = {"REGISTER", "UNDO"}

    _collection = bpy.context.collection
    _objects = bpy.context.selected_objects
    _constraints = []
    MIN_DISTANCE = 0.01

    def execute(self, context):
        props = context.scene.physfxtoolspro_props
        if (props.glue_collection):   
            if self._collection.name == "Scene Collection":
                show_message_box("Uh oh!", "Cannot glue 'Scene Collection'!", "ERROR")
                return {'CANCELLED'}
            else:
                self._objects = self._collection.objects
                gluecollectionname = self._collection.name + "_glue"
        else:
            gluecollectionname = "_glue"

        for idx, obj_a in enumerate(self._objects):
            if (obj_a.type == "MESH"):
                for _, obj_b in self._objects:
                    if (obj_b.type == "MESH" and obj_a.name != obj_b.name):
                        print(obj_a.name, obj_b.name)
                        obj_a_intersection, obj_a_intersection_point = obj_a.ray_cast(obj_a.location, obj_b.location)
                        obj_b_intersection, obj_b_intersection_point = obj_b.ray_cast(obj_b.location, obj_a.location)

                        if (obj_a_intersection and obj_b_intersection):
                            if (obj_a_intersection_point.location - obj_b_intersection_point.location) <= self.MIN_DISTANCE:
                                name = f"Glue-[{obj_a.name}, {obj_b.name}]"
                                for other_obj in context.scene.objects:
                                    if (other_obj.name == name):
                                        bpy.data.objects.remove(other_obj, do_unlink=True)
                                        break

                                mesh = bpy.data.meshes.new(name)
                                constraint_obj = bpy.data.objects.new(name, mesh)
                                constraint_obj.color = (1, 1, 1, 1)
                                constraint_obj.display_type = 'WIRE'

                                constraint_mesh = bmesh.from_edit_mesh(constraint_obj.data)
                                constraint_mesh.verts.new(obj_a.location)
                                constraint_mesh.verts.new(obj_b.location)
                                constraint_mesh.edges.new(constraint_mesh.verts[0], constraint_mesh.verts[1])
                                bmesh.update_edit_mesh(constraint_obj.data)

                                context.view_layer.objects.active = constraint_mesh
                                bpy.ops.rigidbody.constraint_add()
                                constraint = constraint_mesh.rigid_body_constraint
                                constraint.types = 'FIXED'
                                constraint.object1 = obj_a
                                constraint.object2 = obj_b
                                if (props.breaking_threshold == -1):
                                    constraint.use_breaking = False
                                else:
                                    constraint.use_breaking = True
                                    constraint.breaking_threshold = props.breaking_threshold

                                self._constraints.append(constraint_obj)

        gluecollection = bpy.data.collections.get(gluecollectionname)
        if gluecollection is None:
            gluecollection = bpy.data.collections.new(gluecollectionname)
        
        for obj in self._constraints:
            gluecollection.link(obj)

        if gluecollectionname not in self._collection:
            self._collection.children.link(gluecollection)
        return {'FINISHED'}

class PhysFXToolsPro_OT_DeleteGlue(Operator):
    bl_label = "Delete Glue"
    bl_idname = 'physfxtoolspro.deleteglue'
    bl_description = "Delete glue constraints inside the active collection."
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
            if _collection.name.endswith("_glue"):
                for obj in _collection.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                bpy.data.collections.remove(_collection)
        return {'FINISHED'}