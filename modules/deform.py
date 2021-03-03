import bpy
import os
import shutil
from props import parent_path
from bpy.types import Operator, Menu
from bl_operators.presets import AddPresetBase
from modules.funcs import PRESETS_DIR, show_message_box

class PhysFXToolsPro_OT_AddSoftBody(Operator):
    bl_label = 'Add Softbody'
    bl_idname = 'physfxtoolspro.addsoftbody'
    bl_description = 'Add a soft body modifier to the selected object.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = context.active_object
        if (active_object is not None):
            bpy.ops.object.modifier_add(type="SOFT_BODY")
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No active object selected!", icon="ERROR")
            return {'CANCELLED'}

class PhysFXToolsPro_OT_RemoveSoftBody(Operator):
    bl_label = 'Remove Softbody'
    bl_description = 'Remove the soft body modifier from the selected object.'
    bl_idname = 'physfxtoolspro.deletesoftbody'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = context.active_object
        if (active_object is not None):
            bpy.ops.object.modifier_remove(modifier="Softbody")
            return {'FINISHED'}
        else:
            show_message_box("Uh oh!", "No active object selected!", icon="ERROR")
            return {'CANCELLED'}

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

class PhysFXToolsPro_OT_ImportCellFracturePresets(Operator):
    bl_label = 'Import Cell Fracture Presets'
    bl_idname = 'physfxtoolspro.importcellfracturepresets'
    bl_description = 'Import custom cell fracture presets.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        home_path = os.path.join(parent_path, 'presets', 'cellfracture')
        target_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'presets', 'operator', 'object.add_fracture_cell_objects')

        if not os.path.isdir(target_path):
            show_message_box("Uh oh!", "Couldn't find the cell fracture preset folder.", icon="ERROR")
            return {'CANCELLED'}
        else:
            for file in os.listdir(home_path):
                shutil.copy2(os.path.join(home_path, file), target_path)
            return {'FINISHED'}