import ezdxf
from svgpathtools import svg2paths2


def svg_path_to_dxf_with_svgpathtools(svg_file, dxf_file, sampling_interval=0.01):
    # SVGパスの取得
    paths, attributes, svg_attributes = svg2paths2(svg_file)

    # DXFファイルの作成
    doc_dxf = ezdxf.new()
    msp = doc_dxf.modelspace()

    for path in paths:
        points = []
        # SVGパスをサンプリング
        for segment in path:
            num_points = max(int(segment.length() / sampling_interval), 2)
            sampled_points = [
                segment.point(i / (num_points - 1)) for i in range(num_points)
            ]
            points.extend(sampled_points)

        # ポリラインとしてDXFに追加
        if points:
            polyline = msp.add_lwpolyline(
                [(p.real, p.imag) for p in points], close=False
            )
            polyline.dxf.layer = "SVG_PATH"

    # DXFファイルを保存
    doc_dxf.saveas(dxf_file)


# 使用例
svg_path_to_dxf_with_svgpathtools(
    "winter-ornament/winter-ornament-path_test01.svg", "output.dxf"
)
