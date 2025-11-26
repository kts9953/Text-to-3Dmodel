import bpy
import sys

def build_scene():
    # === USER CODE START ===
    # Trunk
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2.5, location=(0, 0, 1.25))
    trunk = bpy.context.active_object
    trunk.name = "Tree_Trunk"

    trunk_mat = bpy.data.materials.new(name="Trunk_Mat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.3, 0.2, 0.1, 1)
    trunk.data.materials.append(trunk_mat)

    # Branches
    for i, angle in enumerate(range(0, 360, 45)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.0, location=(0, 0, 2.0))
        branch = bpy.context.active_object
        branch.name = f"Branch_{i}"
        branch.rotation_euler[1] = 1.0  # tilt upward
        branch.rotation_euler[2] = angle * 3.14159 / 180  # rotate around Z
        branch.data.materials.append(trunk_mat)

    # Foliage
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(0, 0, 3.2))
    leaves = bpy.context.active_object
    leaves.name = "Leaves"

    leaf_mat = bpy.data.materials.new(name="Leaf_Mat")
    leaf_mat.use_nodes = True
    bsdf = leaf_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.1, 0.5, 0.1, 1)
    leaves.data.materials.append(leaf_mat)

    # Apples
    for i, (x, y) in enumerate([(-0.5, 0.2), (0.3, -0.4), (0.6, 0.3)]):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(x, y, 3.0))
        apple = bpy.context.active_object
        apple.name = f"Apple_{i}"
        apple_mat = bpy.data.materials.new(name="Apple_Mat")
        apple_mat.use_nodes = True
        bsdf = apple_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.8, 0.0, 0.0, 1)
        apple.data.materials.append(apple_mat)
    # === USER CODE END ===


def main(output_path: str):
    # 1) 씬 초기화 (딱 한 번)
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2) glTF 익스포터 애드온 활성화
    try:
        bpy.ops.preferences.addon_enable(module="io_scene_gltf2")
    except Exception as e:
        print("[BlenderScript] Failed to enable glTF addon:", e)

    # 3) 유저가 정의한 씬 빌드
    build_scene()

    # 4) GLB로 익스포트
    
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_cameras=False,
        export_lights=False,
        use_selection=False,
    )


if __name__ == "__main__":
    argv = sys.argv

    # 안전하게 argv 파싱
    out = "output.glb"
    if "--" in argv:
        idx = argv.index("--") + 1
        if idx < len(argv):
            out = argv[idx]

    main(out)
