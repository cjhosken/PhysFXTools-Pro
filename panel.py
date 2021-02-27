import bpy
from bpy.types import Panel
from bl_ui.utils import PresetPanel

class PhysFXToolsPro_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PhysFX Tools Pro"

class PhysFXToolsPro_PT_BasePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "PhysFX Tools Pro"
    bl_idname = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        pass

class PhysFXToolsPro_PT_GluePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Glue"
    bl_idname = "PANEL_PT_physfxtoolspro_glue"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        row.prop(props, "glue_collection", text="Use Collection")

        row = layout.row()
        row.prop(props, "breaking_threshold", text="Strength")
        
        row = layout.row()
        row.prop(props, "glue_distance", text="Distance")

        row = layout.row()
        row.operator("physfxtoolspro.gluebodies", text="Glue", icon="MOD_NOISE")
        row.operator("physfxtoolspro.deleteglue", text="", icon='X')

class PhysFXToolsPro_PT_ProxyMeshPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Proxy Mesh"
    bl_idname = "PANEL_PT_physfxtoolspro_proxymesh"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        row.prop(props, "proxy_resolution", text="Resolution")

        row = layout.row()
        row.prop(props, "proxy_offset", text="Offset")

        row = layout.row()
        row.operator("physfxtoolspro.makeproxymesh", text="Create Proxy", icon='MOD_MESHDEFORM')

class PhysFXToolsPro_PT_GroupingBasePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Grouping"
    bl_idname = "PANEL_PT_physfxtoolspro_groupingbase"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        pass

class PhysFXToolsPro_PT_GroupCollisionsPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Collisions"
    bl_idname = "PANEL_PT_physfxtoolspro_groupcollisions"
    bl_parent_id = "PANEL_PT_physfxtoolspro_groupingbase"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text = "Particles")
        col.prop(props, "particle_friction", text="Friction")
        col.prop(props, "particle_damping", text="Damping")
        col.prop(props, "particle_random", text="Random")
        col.prop(props, "kill_particles", text="Kill Particles")

        row = layout.row()
        col = row.column()
        col.label(text = "Cloth")
        col.prop(props, "cloth_friction", text="Friction")
        col.prop(props, "cloth_damping", text="Damping")
        col.prop(props, "cloth_thickness", text="Thickness")

        row = layout.row()
        row.operator("physfxtoolspro.groupcollisions", text="Group Collisions")
        row.operator("physfxtoolspro.deletecollisions", text="", icon="PANEL_CLOSE")

class PhysFXToolsPro_PT_GroupRigidBodiesPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Rigid Bodies"
    bl_idname = "PANEL_PT_physfxtoolspro_grouprigidbodies"
    bl_parent_id = "PANEL_PT_physfxtoolspro_groupingbase"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Settings")
        col.prop(props, 'rigidbody_shape', text="Shape")
        col.prop(props, 'rigidbody_source', text="Source")
        col.prop(props, 'rigidbody_mass', text="Mass")
        col.prop(props, 'rigidbody_friction', text="Friction")
        col.prop(props, 'rigidbody_bounce', text="Bounciness")
        col.prop(props, 'rigidbody_margin', text="Margin")

        row = layout.row()
        row.operator("physfxtoolspro.grouprigidbodies", text="Group Rigid Bodies")
        row.operator("physfxtoolspro.deleterigidbodies", text="", icon="PANEL_CLOSE")

class PHYSFXTOOLSPRO_PT_SoftbodyPresets(PresetPanel, Panel):
    bl_label = "Softbody Presets"
    preset_subdir = 'physfxtoolspro/softbodies'
    preset_operator = 'script.execute_preset'
    preset_add_operator = 'physfxtoolspro.addsoftbodypreset'

class PhysFXToolsPro_PT_SoftbodyPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Soft Body Presets"
    bl_idname = "PANEL_PT_physfxtoolspro_deform"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        obj = context.active_object
        softbody_active = False
        for mod in obj.modifiers:
            if mod.type == "SOFT_BODY":
                softbody_active = True

        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.operator("physfxtoolspro.addsoftbody", text="Add Softbody")
        row.operator("physfxtoolspro.deletesoftbody", text="", icon="PANEL_CLOSE")

        row = layout.row()
        row.label(text="Presets: ")
        PHYSFXTOOLSPRO_PT_SoftbodyPresets.draw_panel_header(row)
        row.enabled = (softbody_active)

class PhysFXToolsPro_PT_ExtraPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Extra"
    bl_idname = "PANEL_PT_physfxtoolspro_extra"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        pass