from bpy.types import Panel

class PhysFXTools_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PhysFXTools"

class PhysFXTools_PT_BasePanel(PhysFXTools_PT_Panel, Panel):
    bl_label = 'PhysFX Tools'
    bl_idname = "PANEL_PT_physfxtools"

    def draw(self, context):
        pass

class PhysFXTools_PT_Glue_Panel(PhysFXTools_PT_Panel, Panel):
    bl_label = 'Glue'
    bl_idname = "PANEL_PT_physfxtoolsglue"
    bl_parent_id = "PANEL_PT_physfxtools"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        row = layout.row()
        layout.prop(scene.physfxtools_settings, "is_breakable", text="Breakable")

        row = layout.row()
        row.prop(scene.physfxtools_settings, "breaking_threshold", text="Threshold",)
        row.enabled = scene.physfxtools_settings.is_breakable

        row = layout.row()
        row.prop(scene.physfxtools_settings, "glue_distance", text="Distance")
        
        row = layout.row()
        row.operator("physfxtools.gluebodies", text="Glue", icon='MOD_NOISE')
        row.operator("physfxtools.deleteglue", text="", icon='X')


class PhysFXTools_PT_ProxyMesh_Panel(PhysFXTools_PT_Panel, Panel):
    bl_label = 'Proxy Mesh'
    bl_idname = "PANEL_PT_physfxtoolsproxymesh"
    bl_parent_id = "PANEL_PT_physfxtools"
        
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        layout.prop(scene.physfxtools_settings, "proxy_resolution", text="Resolution")

        row = layout.row()
        layout.prop(scene.physfxtools_settings, "proxy_distance", text="Offset")

        row = layout.row()
        row.operator("physfxtools.proxymesh", text="Create Proxy", icon='MOD_MESHDEFORM')

class PhysFXTools_PT_CollisionGrouping_Panel(PhysFXTools_PT_Panel, Panel):
    bl_label = 'Collision Grouping'
    bl_idname = "PANEL_PT_physfxtoolscollisiongrouping"
    bl_parent_id = "PANEL_PT_physfxtools"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        layout.prop(scene.physfxtools_settings, "collision_friction", text="Friction")

        row = layout.row()
        layout.prop(scene.physfxtools_settings, "collision_damping", text="Damping")

        row = layout.row()
        row.operator("physfxtools.groupcollisions", text="Group Collisions", icon="MOD_PHYSICS")
        row.operator("physfxtools.deletegroupcollisions", text="", icon="X")
