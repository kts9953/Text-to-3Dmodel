import bpy
import sys

def build_scene():
    # 초기화: 빈 씬으로 시작
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # === USER CODE START ===
    Here is the Python code that will build a table with four legs in Blender using bpy scripting:

        # === USER CODE START ===
        import math

        def add_table():
            table = bpy.data.meshes.new("Table")
            table_obj = bpy.data.objects.new("Table", table)

            vertices = [
                (-0.5, -0.5, 0),
                (0.5, -0.5, 0),
                (0.5, 0.5, 0),
                (-0.5, 0.5, 0)
            ]

            edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

            for v in vertices:
                table.loops.add()
                table.vertices.add()
                table.loops[-1].vertex_index = table.vertices.new(*v)

            for edge in edges:
                table.edges.add()
                table.edges[-1].vertices = [table.loops[edge[0]].vertex_index, table.loops[edge[1]].vertex_index]

            table_obj.location = (0, 0, 0)
            bpy.context.collection.objects.link(table_obj)
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
