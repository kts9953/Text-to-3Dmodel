# Seat
bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, 0, 0.6))
seat = bpy.context.active_object
seat.scale[2] = 0.2
seat.name = "Seat"

# Backrest
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.5, 1.1))
backrest = bpy.context.active_object
backrest.scale[0] = 0.6
backrest.scale[2] = 0.5
backrest.name = "Backrest"

# Left armrest
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.65, 0, 0.9))
arm_L = bpy.context.active_object
arm_L.scale[0] = 0.1
arm_L.scale[1] = 0.5
arm_L.scale[2] = 0.4
arm_L.name = "Armrest_Left"

# Right armrest
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.65, 0, 0.9))
arm_R = bpy.context.active_object
arm_R.scale[0] = 0.1
arm_R.scale[1] = 0.5
arm_R.scale[2] = 0.4
arm_R.name = "Armrest_Right"

# Legs
leg_positions = [(0.45, 0.45, 0.3), (-0.45, 0.45, 0.3), (0.45, -0.45, 0.3), (-0.45, -0.45, 0.3)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=pos)
    leg = bpy.context.active_object
    leg.scale[0] = 0.1
    leg.scale[1] = 0.1
    leg.scale[2] = 0.3
    leg.name = f"Leg_{i}"
""""
