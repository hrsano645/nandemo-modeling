import cadquery as cq
from ocp_vscode import show_object
from pathlib import Path

export_dir = Path(__file__).parent / "export"

# なんらかのモデリング

result = None

# 表示
# show_object(result)

# export: stl
# cq.exporters.export(result, export_dir / "result.stl")

# export: step
# cq.exporters.export(result, export_dir / "result.step")
