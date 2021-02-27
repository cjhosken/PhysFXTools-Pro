import bpy
import os

PRESETS_DIR = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'presets', 'physfxtoolspro')

def show_message_box(title="Message Box", message="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)