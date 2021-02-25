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
    "name": "PhysFX Tools",
    "author": "Christopher Hosken",
    "description": "Useful tools for physics simulations",
    "blender": (2,92,0),
    "version": (4,0),
    "location": "View3D > Properties > PhysFX",
    "wiki_url": "https://github.com/Christopher-Hosken/PhysFX-Tools/wiki",
    "tracker_url" : "https://github.com/Christopher-Hosken/PhysFX-Tools/issues",
    "category": "Animation",
}

import bpy
import sys
import os
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
    'props',
    'ops',
    'panel',
]

for module_name in module_list:
    if (module_name in sys.modules):
        reload(sys.modules[module_name])

import props
import ops
import panel

classes = [
    props.PhysFXToolsProperties,
    ops.PhysFXTools_OT_Glue,
    ops.PhysFXTools_OT_DeleteGlue,
    ops.PhysFXTools_OT_ProxyMesh,
    ops.PhysFXTools_OT_GroupCollisions,
    ops.PhysFXTools_OT_DeleteGroupCollisions,
    panel.PhysFXTools_PT_BasePanel,
    panel.PhysFXTools_PT_Glue_Panel,
    panel.PhysFXTools_PT_ProxyMesh_Panel,
    panel.PhysFXTools_PT_CollisionGrouping_Panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.physfxtools_settings = bpy.props.PointerProperty(type=props.PhysFXToolsProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.physfxtools_settings

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()