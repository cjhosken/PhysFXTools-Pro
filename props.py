from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty, IntProperty, FloatProperty
import __init__

parent_path = __init__.parent_path

class PhysFXToolsPro_Properties(PropertyGroup):
    glue_collection : BoolProperty(
        name = "Glue Collection",
        description= "Glue objects in active collection instead of selected objects.",
        default = False,
    )

    breaking_threshold : FloatProperty(
        name = "Breaking Threshold",
        description= "Threshold value used to determine the strength at which glue will break. -1 will make glue indestructable.",
        default = -1,
        min = -1,
    )

    glue_distance : FloatProperty(
        name = "Glue Distance",
        description = "Max distance between glueable objects.",
        default = 1,
        min = 0,
    )

    proxy_resolution : IntProperty(
        name = "Proxy Resolution",
        description = "Resolution of proxy mesh.",
        default = 4,
        min = 1,
        max = 6,
    )

    proxy_offset : FloatProperty(
        name = "Proxy Offset",
        description = "Amount of space between base mesh and proxy.",
        default = 0.1,
        min = 0,
    )

    particle_friction : FloatProperty(
        name = "Particle Friction",
        description = "Amount of friction during particle collision.",
        min = 0,
        max = 1,
        default = 0,
    )

    particle_damping : FloatProperty(
        name = "Particle Damping",
        description = "Amount of damping during particle collision.",
        min = 0,
        max = 1,
        default = 0,
    )

    particle_random : FloatProperty(
        name = "Particle Random",
        description = "Random variation of friction and damping",
        min = 0,
        max = 1,
        default = 0,
    )

    kill_particles : BoolProperty(
        name = "Kill Particles",
        description = "Kill collided particles.",
        default = False,
    )

    cloth_friction : FloatProperty(
        name = "Cloth Friction",
        description = "Friction for cloth collisions",
        min = 0,
        max = 80,
        default = 5,
    )

    cloth_damping : FloatProperty(
        name = "Cloth Damping",
        description = "Amount of damping for cloth collisions",
        min = 0,
        max = 1,
        default = 0,
    )

    cloth_thickness : FloatProperty(
        name = "Thickness",
        description = "Outer thickness of object.",
        min = 0,
        max = 1,
        default = 0.02,
    )

    rigidbody_is_active : BoolProperty(
        name = "Rigidbody Type",
        description = "Role of object in rigidbody simulations.",
        default = True,
    )

    rigidbody_mass : FloatProperty(
        name = "Rigidbody Mass",
        description = "",
        min = 0,
        default = 1,
    )

    rigidbody_shape : EnumProperty(
        name = "Rigidbody Shape",
        description="",
        items = [
            ("COMPOUND", "Compound Parent", ""),
            ("MESH", "Mesh", ""),
            ("CONVEX_HULL", "Convex Hull", ""),
            ("CONE", "Cone", ""),
            ("CYLINDER", "Cylinder", ""),
            ("CAPSULE", "Capsule", ""),
            ("SPHERE", "Sphere", ""),
            ("BOX", "Box", ""),
        ],
        default="CONVEX_HULL",
    )

    rigidbody_source : EnumProperty(
        name = "Rigidbody Shape",
        description="",
        items = [
            ("BASE", "Base", ""),
            ("DEFORM", "Deform", ""),
            ("FINAL", "Final", ""),
        ],
        default = "BASE",
    )

    rigidbody_friction : FloatProperty(
        name = "Rigidbody Friction",
        description = "Resistance of object to movement.",
        min = 0,
        max = 1,
        default = 0.5,
    )

    rigidbody_bounce : FloatProperty(
        name = "Rigidbody Bounciness",
        description = "Tendency of object to bounce after collision (0 = stays still, 1 = perfectly elastic).",
        min = 0,
        max = 1,
        default = 0.5,
    )

    rigidbody_margin : FloatProperty(
        name = "Rigidbody Margin",
        description = "Threshold of distance where collisions are still considered.",
        min = 0,
        default = 0.04,
    )