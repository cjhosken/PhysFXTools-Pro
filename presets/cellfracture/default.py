import bpy
op = bpy.context.active_operator

op.source = {'VERT_OWN'}
op.source_limit = 100
op.source_noise = 1.0
op.cell_scale = (1.0, 1.0, 1.0)
op.recursion = 0
op.recursion_source_limit = 8
op.recursion_clamp = 250
op.recursion_chance = 0.25
op.recursion_chance_select = 'RANDOM'
op.use_smooth_faces = False
op.use_sharp_edges = True
op.use_sharp_edges_apply = True
op.use_data_match = True
op.use_island_split = True
op.margin = 0.0010000000474974513
op.material_index = 0
op.use_interior_vgroup = False
op.mass_mode = 'VOLUME'
op.mass = 1.0
op.use_recenter = True
op.use_remove_original = True
op.collection_name = 'Fracture'
op.use_debug_points = False
op.use_debug_redraw = True
op.use_debug_bool = False
