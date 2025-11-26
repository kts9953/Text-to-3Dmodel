# Seat base

bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, 0, 0.6))
seat = bpy.context.active_object
seat.scale[2] = 0.2

seat_mat = bpy.data.materials.new(name="Seat_Mat")
seat_mat.use_nodes = True
seat_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.4, 0.2, 0.1, 1)
seat.data.materials.append(seat_mat)

# Backrest

bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, -0.5, 1.0))
back = bpy.context.active_object
back.scale[0] = 0.9
back.scale[2] = 0.6
back.data.materials.append(seat_mat)

# Left armrest

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.65, 0, 0.9))
arm_l = bpy.context.active_object
arm_l.scale[0] = 0.1
arm_l.scale[1] = 0.4
arm_l.scale[2] = 0.5
arm_l.data.materials.append(seat_mat)

# Right armrest

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.65, 0, 0.9))
arm_r = bpy.context.active_object
arm_r.scale[0] = 0.1
arm_r.scale[1] = 0.4
arm_r.scale[2] = 0.5
arm_r.data.materials.append(seat_mat)

# Chair legs

for x in [-0.5, 0.5]:
for y in [-0.4, 0.4]:
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.6, location=(x, y, 0.3))
leg = bpy.context.active_object
leg.data.materials.append(seat_mat)
