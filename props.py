from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntProperty, FloatProperty

class PhysFXToolsProperties(PropertyGroup):
    breaking_threshold: FloatProperty(
        name = "Breaking Threshold",
        default = 10,
        min = 0,
        description = "Impluse threshold needed for the glue to break."
    )
    
    glue_distance: FloatProperty(
        name="Glue Distance",
        default = 0.1,
        min = 0,
        max = 1000,
        description = "Maximum gluing distance between selected objects"
    )

    is_breakable: BoolProperty(
        name="Is Breakable",
        description="Determines whether the glue can be broken or not.",
        default = True
    )

    proxy_distance: FloatProperty(
        name = "Proxy Distance",
        default = 0,
        min = 0,
        description = "Distance to keep from the target mesh."
    )

    proxy_resolution: IntProperty(
        name = "Proxy Resolution",
        default = 5,
        min = 0,
        max = 10,
        description = "Resolution of the proxy mesh."
    )
    
    collision_friction: FloatProperty(
        name="Collision Friction",
        default = 0,
        min = 0,
        max = 1,
        description = "Amount of friction for all objects in the selected group."
    )
    
    collision_damping: FloatProperty(
        name="Collision Damping",
        default = 0,
        min = 0,
        max = 1,
        description = "Amount of collision damping for all objects in the selected group."
    )