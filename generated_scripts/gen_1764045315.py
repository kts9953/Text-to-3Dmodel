import bpy
import sys

def build_scene():
    # 초기화: 빈 씬으로 시작
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # === USER CODE START ===
    # Trunk
    bpy.ops.mesh.primitive_cylinder_add(
    radius=0.15,
    depth=2.0,
    location=(0.0, 0.0, 1.0)
    )
    trunk = bpy.context.active_object
    trunk.name = "Tree_Trunk"

    trunk_mat = bpy.data.materials.new(name="Tree_Trunk_Mat")
    trunk_mat.use_nodes = True
    trunk_bsdf = trunk_mat.node_tree.nodes.get("Principled BSDF")
    if trunk_bsdf is not None:
        trunk_bsdf.inputs["Base Color"].default_value = (0.25, 0.16, 0.08, 1.0)
    trunk_bsdf.inputs["Roughness"].default_value = 0.7
    trunk.data.materials.append(trunk_mat)

    # Foliage (cone)
    bpy.ops.mesh.primitive_cone_add(
    radius1=0.9,
    radius2=0.0,
    depth=1.8,
    location=(0.0, 0.0, 2.2)
    )
    foliage = bpy.context.active_object
    foliage.name = "Tree_Foliage"

    foliage_mat = bpy.data.materials.new(name="Tree_Foliage_Mat")
    foliage_mat.use_nodes = True
    foliage_bsdf = foliage_mat.node_tree.nodes.get("Principled BSDF")
    if foliage_bsdf is not None:
    foliage_bsdf.inputs["Base Color"].default_value = (0.05, 0.4, 0.08, 1.0)
    foliage_bsdf.inputs["Roughness"].default_value = 0.5
    foliage.data.materials.append(foliage_mat)
    # === USER CODE END ===

def main(output_path: str):
    build_scene()
    # glb로 익스포트 (Blender 5 기준)
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_cameras=False,
        export_lights=False,
    )

if __name__ == "__main__":
    argv = sys.argv
    out = argv[argv.index("--") + 1]
    main(out)
