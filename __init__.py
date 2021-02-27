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

__copyright__ = "(c) 2021,  Christopher Hosken"
__license__ = "GPL v3"

bl_info= {
    "name": "PhysFX Tools Pro",
    "author": "Christopher Hosken",
    "description": "Convenient tools for Blender physics simulations",
    "blender": (2,92,0),
    "version": (5,0),
    "location": "View3D > Properties > PhysFX Tools Pro",
    "wiki_url": "https://github.com/Christopher-Hosken/PhysFX-Tools/wiki",
    "tracker_url" : "https://github.com/Christopher-Hosken/PhysFX-Tools/issues",
    "category": "Animation",
}

import bpy
import sys
import os
import shutil
from importlib import reload
parent_path = None

try:
    parent_path = os.path.dirname(__file__)
except:
    pass
try:
    parent_path = os.path.dirname(bpy.context.space_data.text.filepath)
except:
    pass

if (parent_path is None):
    raise FileNotFoundError("Cannot locate path, 'parent_path'.")

sys.path.append(parent_path)

module_list = [
    "funcs",
    "props",
    "glue",
    "grouping",
    "proxymesh",
    "deform",
    "panel"
]

for module_name in module_list:
    if (module_name in sys.modules):
        reload(sys.modules[module_name])

import modules.funcs as funcs
import props
import modules.glue as glue
import modules.grouping as grouping
import modules.proxymesh as proxymesh
import modules.deform as deform
import panel

from modules.funcs import PRESETS_DIR

package_path = os.path.join(parent_path, 'presets')

if not os.path.isdir(PRESETS_DIR):
    os.makedirs(PRESETS_DIR)

for folder in os.listdir(package_path):
    if not os.path.isdir(os.path.join(PRESETS_DIR, folder)):
        os.makedirs(os.path.join(PRESETS_DIR, folder))
    for file in os.listdir(os.path.join(package_path, folder)):
        shutil.copy2(os.path.join(package_path, folder, file), os.path.join(PRESETS_DIR, folder))

classes = [
    glue.PhysFXToolsPro_OT_GlueBodies,
    glue.PhysFXToolsPro_OT_DeleteGlue,
    grouping.PhysFXToolsPro_OT_GroupCollisions,
    grouping.PhysFXToolsPro_OT_DeleteCollisions,
    grouping.PhysFXToolsPro_OT_GroupRigidBodies,
    grouping.PhysFXToolsPro_OT_DeleteRigidBodies,
    proxymesh.PhysFXToolsPro_OT_MakeProxyMesh,
    deform.PhysFXToolsPro_OT_AddSoftBody,
    deform.PhysFXToolsPro_OT_RemoveSoftBody,
    deform.PHYSFXTOOLSPRO_MT_SoftBodyPresets,
    deform.PhysFXToolsPro_OT_AddSoftBodyPreset,
    panel.PhysFXToolsPro_PT_BasePanel,
    panel.PhysFXToolsPro_PT_GluePanel,
    panel.PhysFXToolsPro_PT_ProxyMeshPanel,
    panel.PhysFXToolsPro_PT_GroupingBasePanel,
    panel.PhysFXToolsPro_PT_GroupCollisionsPanel,
    panel.PhysFXToolsPro_PT_GroupRigidBodiesPanel,
    panel.PHYSFXTOOLSPRO_PT_SoftbodyPresets,
    panel.PhysFXToolsPro_PT_SoftbodyPanel,
    panel.PhysFXToolsPro_PT_ExtraPanel,
    props.PhysFXToolsPro_Properties,   
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.physfxtoolspro_props = bpy.props.PointerProperty(type=props.PhysFXToolsPro_Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.physfxtoolspro_props

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()