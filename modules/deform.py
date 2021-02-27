import bpy
from bpy.types import Operator, Menu
from bl_operators.presets import AddPresetBase
from modules.funcs import PRESETS_DIR, show_message_box

class PhysFXToolsPro_OT_AddSoftBody(Operator):
    bl_label = 'Add Softbody'
    bl_idname = 'physfxtoolspro.addsoftbody'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_selection = context.active_object
        if (active_selection is not None):
            bpy.ops.object.modifier_add(type="SOFT_BODY")
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No active object selected!", icon="ERROR")
        return {'FINISHED'}

class PhysFXToolsPro_OT_RemoveSoftBody(Operator):
    bl_label = 'Remove Softbody'
    bl_idname = 'physfxtoolspro.deletesoftbody'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_selection = context.active_object
        if (active_selection is not None):
            bpy.ops.object.modifier_remove(modifier="Softbody")
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No active object selected!", icon="ERROR")
        return {'FINISHED'}

class PHYSFXTOOLSPRO_MT_SoftBodyPresets(Menu):
    bl_label = 'Softbody Presets'
    preset_subdir = 'physfxtoolspro/softbodies'
    preset_operator = 'script.execute_preset'
    draw = Menu.draw_preset

class PhysFXToolsPro_OT_AddSoftBodyPreset(AddPresetBase, Operator):
    bl_label = 'Add Softbody Preset'
    bl_idname = 'physfxtoolspro.addsoftbodypreset'
    preset_menu = 'PHYSFXTOOLSPRO_MT_SoftBodyPresets'

    preset_defines = [
        'obj = bpy.context.object',
        'scene = bpy.context.scene',
        'softbody = obj.modifiers["Softbody"]'
    ]

    preset_values = [
        'softbody.settings.friction',
        'softbody.settings.mass',
        'softbody.settings.use_goal',
        'softbody.settings.goal_spring',
        'softbody.settings.goal_friction',
        'softbody.settings.goal_default',
        'softbody.settings.goal_min',
        'softbody.settings.goal_max',
        'softbody.settings.use_edges',
        'softbody.settings.pull',
        'softbody.settings.push',
        'softbody.settings.damping',
        'softbody.settings.plastic',
        'softbody.settings.bend',
        'softbody.settings.spring_length',
        'softbody.settings.use_edge_collision',
        'softbody.settings.use_face_collision',
        'softbody.settings.aerodynamics_type',
        'softbody.settings.aero',
        'softbody.settings.use_stiff_quads',
        'softbody.settings.shear',
        'softbody.settings.use_self_collision',
        'softbody.settings.collision_type',
        'softbody.settings.ball_size',
        'softbody.settings.ball_stiff',
        'softbody.settings.ball_damp',
    ]

    preset_subdir = 'physfxtoolspro/softbodies'