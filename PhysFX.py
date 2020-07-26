#    PhysFX Tools is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PhysFX Tools is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

__copyright__ = "(c) 2020,  Christopher Hosken"
__license__ = "GPL v3"

bl_info= {
    "name": "PhysFX Tools",
    "author": "Christopher Hosken",
    "version": (2,0),
    "blender": (2,80,3),
    "location": "View3D > Properties > PhysFX",
    "description": "Useful tools for physics simulations",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy, sys
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import FloatProperty, IntProperty, BoolProperty, PointerProperty
from mathutils import Vector
##############################################

class Mysettings(PropertyGroup):
    BreakingThreshold: FloatProperty(
        name = "Threshold",
        default = 10,
        min = 0,
        max = 21000000,
        description = "Impluse threshold that must be reached for the glue to break."
    )
    
    GlueDistance: FloatProperty(
        name="Glue Distance",
        default = 0.1,
        min = 0,
        max = 1000,
        description = "Maximum gluing distance"
    )

    Breakable: BoolProperty(
        name="Break_Bool",
        description="Determines whether the glue can be broken or not.",
        default = True
    )

    ProxyDistance: FloatProperty(
        name = "proxydis",
        default = 0,
        min = 0,
        max = 21000000,
        description = "Distance to keep from the target object."
    )

    ProxyResolution: IntProperty(
        name = "proxyres",
        default = 5,
        min = 0,
        max = 10,
        description = "Resolution of the proxy mesh."
    )
    
    ColFric: FloatProperty(
        name="colfric",
        default = 0,
        min = 0,
        max = 1,
        description = "Amount of friction during collisions."
    )
    
    ColDamp: FloatProperty(
        name="coldamp",
        default = 0,
        min = 0,
        max = 1,
        description = "Amount of damping during collisions."
    )

################################################

def arrdiff(x, y):
    return (x - y).normalized()

def ShowMessageBox(message="Message to give", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

#Glue Code
class Glue(Operator):
    bl_idname = 'glue.bodies'
    bl_label = 'Glue'
    bl_description = 'Glues rigid bodies together'
    bl_options = {'REGISTER', 'UNDO'}

    def execute (self, context):
        depsgraph = context.evaluated_depsgraph_get()
        #Selects all objects in the specified collection
        test = bpy.context.collection
        name = test.name
        
        if name=="Master Collection":
            ShowMessageBox("Please select a collection to glue.","No Collection Selected!", 'ERROR')
            return({'CANCELLED'})

        colname = name + '_constraints'

        if bpy.context.scene.rigidbody_world is None:
            ShowMessageBox("Please create a rigid body world.","No Rigid Body World!", 'ERROR')
            return({'CANCELLED'})

        #Creates a rigidbody world
        if bpy.context.scene.rigidbody_world.enabled is False:
            ShowMessageBox("Please create a rigid body world.","No Rigid Body World!", 'ERROR')
            return({'CANCELLED'})
        
        else:
            #Delete Duplicate Collections/Constraints
            concoll = bpy.data.collections.get(colname)
            if concoll is not None:
                for o in concoll.objects:
                    bpy.data.objects.remove(o, do_unlink=True)
            else:
                concoll = bpy.data.collections.new(colname)

            for i, left in enumerate(test.objects):
                if left.type != "MESH": continue
                l = depsgraph.objects.get(left.name, None)
                if l is None: continue
                lm = left.matrix_parent_inverse
                for j, right in enumerate(test.objects[i+1:]):
                    if right.type != "MESH": continue
                    r = depsgraph.objects.get(right.name, None)
                    rm = right.matrix_parent_inverse
                    if r is None: continue
                    try:
                        lb, pl = left.ray_cast(left.location - left.location,
                                arrdiff(right.location, left.location), distance=1000000,
                                depsgraph=depsgraph)[:2]
                        rb, pr = right.ray_cast(right.location - right.location,
                                arrdiff(left.location, right.location), distance=1000000,
                                depsgraph=depsgraph)[:2]
                    except RuntimeError:
                        continue
                    pr += r.location
                    pl += l.location
                    if not rb or not lb:
                        continue
                        touching = (pl - pr).length_squared / (left.location - right.location).length_squared
                    if (pl - pr).length_squared < context.scene.glue_settings.GlueDistance:
                        ob = bpy.data.objects.new('Constraint', object_data=None)
                        ob.location = pl
                        context.scene.collection.objects.link(ob)
                        context.view_layer.objects.active = ob
                        bpy.ops.rigidbody.constraint_add()
                        concoll.objects.link(ob)
                        context.scene.collection.objects.unlink(ob)
                        cr = ob.rigid_body_constraint
                        cr.type = 'FIXED'
                        cr.object1 = left
                        cr.object2 = right
                        cr.use_breaking = context.scene.glue_settings.Breakable
                        cr.breaking_threshold = context.scene.glue_settings.BreakingThreshold

            if colname not in test.children:
                test.children.link(concoll)

            self.report({'INFO'}, 'Bodies Glued')
            return {'FINISHED'}

#############################################################

class Delglue(Operator):
    bl_idname = 'del.glue'
    bl_label = 'Del-Glue'
    bl_description = 'Deletes Glue'
    bl_options = {'REGISTER', 'UNDO'}

    def execute (self, context):

    #Deletes Glue
        name = bpy.context.collection.name
        if name.endswith("_constraints"):
            c = bpy.data.collections.get(name)
            for o in c.objects:
                bpy.data.objects.remove(o, do_unlink=True)
            bpy.data.collections.remove(c)
            self.report({'INFO'}, 'Glue Deleted')

    #Delete Glue Error Message
        else:
            ShowMessageBox("Please select a constraint collection to delete.",
                           "No Constraint Collection Selected!", 'ERROR')
        return{'FINISHED'}

###########################################################

class ProxyMesh(Operator):
    bl_idname = "proxy.mesh"
    bl_label  = "ProxyMesh"
    bl_description = "Creates a proxy mesh around a target object"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        base = bpy.context.active_object
        
        if base is None:
            self.report({'INFO'}, 'Collisions Group')
            ShowMessageBox("Please select an object to proxy.",
                               "No Object Selected!", 'ERROR')
                               
        else:
            if base.type != 'MESH':
                ShowMessageBox("Please select an object to proxy.","No Object Selected!", 'ERROR')
            else:
                vx = base.location.x
                vy = base.location.y
                vz = base.location.z
                sx = base.scale.x
                sy = base.scale.y
                sz = base.scale.z
                dx = base.dimensions.x
                dy = base.dimensions.y
                dz = base.dimensions.z

                #CREATES A CUBE
                bpy.ops.mesh.primitive_cube_add(size=2, calc_uvs=True,
    enter_editmode=False, align='WORLD', location=(vx,vy,vz), rotation=(0.0,
    0.0, 0.0))

                #SCALES AND SUBDIVIDES THE CUBE
                object = bpy.context.active_object
                object.name = base.name + '_proxy'
                bpy.ops.transform.resize(value=(dx*sx, dy*sy, dz*sz))
                bpy.ops.object.modifier_add(type='SUBSURF')
                bpy.context.object.modifiers["Subdivision"].subdivision_type ='SIMPLE'
                bpy.context.object.modifiers["Subdivision"].levels = 6
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")

                #SHRINKWRAPS THE CUBE
                bpy.ops.object.modifier_add(type="SHRINKWRAP")
                bpy.context.object.modifiers["Shrinkwrap"].offset = context.scene.proxy_settings.ProxyDistance
                bpy.context.object.modifiers["Shrinkwrap"].target = base
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")

                #REMESHES THE CUBE
                bpy.ops.object.modifier_add(type="REMESH")
                bpy.context.object.modifiers["Remesh"].mode = 'SMOOTH'
                bpy.context.object.modifiers["Remesh"].octree_depth = context.scene.proxy_settings.ProxyResolution
                bpy.context.object.modifiers["Remesh"].use_smooth_shade = True
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

                #Parents the Proxy to the base mesh
                object.parent = base
                object.matrix_parent_inverse = base.matrix_world.inverted()

                self.report({'INFO'}, 'Proxy Created')
            return{'FINISHED'}
        return{'FINISHED'}

###########################################################

class GroupCollisions(Operator):
    bl_idname = "group.collisions"
    bl_label = "GroupCollisions"
    bl_description = "Adds the collision property to selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        objs = bpy.context.selected_objects
        for obj in objs:    
            if obj.type == 'MESH':
                for o in bpy.context.selected_objects:
                    o.modifiers.new(type='COLLISION', name="collision")
                    o.collision.friction_factor = context.scene.col_settings.ColFric
                    o.collision.damping_factor = context.scene.col_settings.ColDamp
                self.report({'INFO'}, 'Collisions Grouped')
                
            else:
                ShowMessageBox("Please select an object to add collisions to.","No Object Selected!", 'ERROR')
                
            return{'FINISHED'}
        
###########################################################

class DelCollisions(Operator):
    bl_idname = "del.collisions"
    bl_label = "Del-Collisions"
    bl_description = "Deletes the collision propety from selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = bpy.context.selected_objects
        for obj in objs:
        
            if obj.type == 'MESH':
                for o in bpy.context.selected_objects:
                    for m in o.modifiers:
                        if(m.type == "COLLISION"):
                            o.modifiers.remove(m)
                            
            else:
                self.report({'INFO'}, 'Collisions Deleted')
                ShowMessageBox("Please select an object to add collisions to.","No Object Selected!", 'ERROR')
            
        return{'FINISHED'}
        
###########################################################

#Side Panel
class OBJECT_PT_PhysFX(Panel):
    bl_idname = "OBJECT_PT_PhysFX"
    bl_label = "PhysFX Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PhysFX"   
    
    def draw(self, context):
        pass

class OBJECT_PT_Glue(Panel):
    bl_label = 'Glue:'
    bl_parent_id = "OBJECT_PT_PhysFX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "PhysFX"   
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        glue_settings = scene.glue_settings
        
        layout.prop(glue_settings, "Breakable", text="Breakable")
        row = layout.row()
        row.prop(glue_settings, "BreakingThreshold", text="Threshold",)
        row.enabled = context.scene.glue_settings.Breakable
        row = layout.row()
        row.prop(glue_settings, "GlueDistance", text="Distance")
        

        row = layout.row()
        row.operator("glue.bodies", text="Glue", icon='MOD_NOISE')
        row.operator("del.glue", text="", icon='X')

        #Proxy Mesh Generator
class OBJECT_PT_Proxy(Panel):
    bl_label = 'Proxy Mesh:'
    bl_parent_id = "OBJECT_PT_PhysFX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "PhysFX"   
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        proxy_settings = scene.proxy_settings
        
        layout.prop(proxy_settings, "ProxyResolution", text="Resolution")
        row = layout.row()
        layout.prop(proxy_settings, "ProxyDistance", text="Offset")
        row = layout.row()
        row.operator("proxy.mesh", text="Create Proxy", icon='MOD_MESHDEFORM')

        #Collisions
class OBJECT_PT_Group(Panel):
    bl_label = 'Group Collisions:'
    bl_parent_id = "OBJECT_PT_PhysFX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "PhysFX"   
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col_settings = scene.col_settings
        layout.prop(col_settings, "ColFric", text="Friction")
        row = layout.row()
        layout.prop(col_settings, "ColDamp", text="Damping")
        row = layout.row()
        row.operator("group.collisions", text="Group Collisions", icon="MOD_PHYSICS")
        row.operator("del.collisions", text="", icon="X")


def register():
    bpy.utils.register_class(DelCollisions)
    bpy.utils.register_class(GroupCollisions)
    bpy.utils.register_class(Mysettings)
    bpy.types.Scene.glue_settings = PointerProperty(type=Mysettings)
    bpy.types.Scene.proxy_settings = PointerProperty(type=Mysettings)
    bpy.types.Scene.col_settings = PointerProperty(type=Mysettings)
    bpy.utils.register_class(Delglue)
    bpy.utils.register_class(Glue)
    bpy.utils.register_class(ProxyMesh)
    bpy.utils.register_class(OBJECT_PT_PhysFX)
    bpy.utils.register_class(OBJECT_PT_Glue)
    bpy.utils.register_class(OBJECT_PT_Proxy)
    bpy.utils.register_class(OBJECT_PT_Group)


def unregister():
    bpy.utils.unregister_class(DelCollisions)
    bpy.utils.unregister_class(GroupCollisions)
    bpy.utils.unregister_class(Mysettings)
    del bpy.types.Scene.glue_settings
    del bpy.types.Scene.proxy_settings
    del bpy.types.Scene.col_settings
    bpy.utils.unregister_class(Delglue)
    bpy.utils.unregister_class(Glue)
    bpy.utils.unregister_class(ProxyMesh)
    bpy.utils.unregister_class(OBJECT_PT_PhysFX)
    bpy.utils.unregister_class(OBJECT_PT_Glue)
    bpy.utils.unregister_class(OBJECT_PT_Proxy)
    bpy.utils.unregister_class(OBJECT_PT_Group)


if __name__ == "__main__":
    register()