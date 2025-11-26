```python# Seat
bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0.0, 0.0, 0.5))
seat = bpy.context.active_object
seat.scale[2] = 0.2
seat.name = "Seat"

# Backrest
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.45, 1.0))
backrest = bpy.context.active_object
backrest.scale[0] = 0.6
backrest.scale[2] = 0.5
backrest.name = "Backrest"

# Left leg
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(0.45, 0.35, 0.3))
leg_LF = bpy.context.active_object
leg_LF.name = "Leg_LeftFront"

# Right leg
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(-0.45, 0.35, 0.3))
leg_RF = bpy.context.active_object
leg_RF.name = "Leg_RightFront"

# Left back leg
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(0.45, -0.35, 0.3))
leg_LB = bpy.context.active_object
leg_LB.name = "Leg_LeftBack"

# Right back leg
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(-0.45, -0.35, 0.3))
leg_RB = bpy.context.active_object
leg_RB.name = "Leg_RightBack"```
