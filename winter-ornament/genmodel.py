# import numpy as np
import cadquery as cq

# from svgpathtools import svg2paths, Line, CubicBezier
from ocp_vscode import show_object
from pathlib import Path

# exportdir
export_dir = Path(__file__).parent / "export"
export_dir.mkdir(exist_ok=True)

# font filepath
font_path = (Path(__file__).parent / Path("fonts/MPLUSRounded1c-Bold.ttf")).absolute()


def __generate_text_model(text: str, size, x, y, thickness) -> cq.Workplane | None:
    if not text:
        return None
    return (
        cq.Workplane("XY")
        .text(text, size, thickness, fontPath=str(font_path))
        .translate((x, y, 0))
    )


def __generate_base_plate_square(
    width, height, thickness, fillet
) -> cq.Workplane | None:
    """長方形のベースプレートを生成する"""
    return (
        cq.Workplane("XY")
        .box(width, height, thickness)
        .edges("|Z")
        .fillet(fillet)
        # 中心ではなく、左下を原点とする
        .translate((width / 2, height / 2, 0))
    )


# 引数は、全体の大きさ、アーチの高さ、上部の絞り幅、厚さ
def __generate_base_plate_arc_rapezoid(
    width: float, heigth: float, archeigth, upper_sibori, tickness
) -> cq.Workplane | None:
    """台形のベースプレートを生成する。archeigthはアーチの高さで上下に反映、upper_siboriは上部の絞り幅 左右同じ数値となる、ticknessは厚さ
    また、外周は3mmの縁取りを行う。高さはtickness + 3mmとなる。
    """

    def __generate_wire() -> cq.Workplane | None:
        """ワイヤーを生成する"""
        center_x = width / 2
        arc_upper_y = heigth - archeigth
        sibori_rigth = width - upper_sibori
        sibori_left = upper_sibori

        return (
            cq.Workplane("XY")
            .moveTo(0, archeigth)
            .threePointArc((center_x, 0), (width, archeigth))
            .lineTo(sibori_rigth, arc_upper_y)
            .threePointArc((center_x, heigth), (sibori_left, arc_upper_y))
            .lineTo(0, archeigth)
            .close()
        )

    # ベースプレートを書いていく
    plate_result = __generate_wire()
    plate_result = plate_result.extrude(tickness + 3)

    # 内側のプレートを生成する
    inner_plate = __generate_wire().offset2D(-2, "intersection")

    # 縁取りを行う
    inner_plate = inner_plate.extrude(3).translate((0, 0, tickness))
    # show_object(inner_plate)
    plate_result = plate_result.cut(inner_plate)

    return plate_result


def __generate_hole_for_string(
    plate_workplace: cq.Workplane, x: float, y: float, radius: float
) -> cq.Workplane | None:
    """紐を取り付ける穴を生成する。plate_workplaceへ直接反映させる。今は中央のみ対応"""
    # TODO: 2024-12-01 中央判定はboundingboxで幅を取得して判定する。当面はx, yを直接指定する
    return (
        plate_workplace.faces(">Z").workplane().center(x, y).circle(radius).cutThruAll()
    )


def generate_holiday_plate(icon_dxf_path: Path, text1, text2):
    """ホリデープレートを生成する 処理のまとめ
    exportpathはplate-{pathのbasename}_{text1}_{test2}の文字列と同じ名前で保存される"""

    # パラメーターを設定
    width = 80
    heigth = 100
    archeigth = 10
    upper_sibori = 15
    tickness = 3

    # 文字の内部パラメーター
    text_size = 8
    text_x = width / 2
    text_tickness = tickness + 3

    # ベースプレートを生成
    plate_result = __generate_base_plate_arc_rapezoid(
        width, heigth, archeigth, upper_sibori, tickness
    )

    # 紐通しの穴
    plate_result = __generate_hole_for_string(
        plate_result,
        width / 2,
        heigth - 8,
        3,
    )

    # dxfファイルを読み込む
    icon_path = cq.importers.importDXF(icon_dxf_path)

    # bounding boxを取得して、中心を移動
    bbox = icon_path.val().BoundingBox()
    # print(f"{bbox.center=} {bbox.xlen=} {bbox.ylen=}")
    translation_vector = cq.Vector(0, 0, 0) - bbox.center

    icon_path = icon_path.translate(translation_vector)

    # 形状を作って移動。
    ornament_obj = (
        cq.Workplane("XY")
        .add(icon_path)
        .toPending()
        .extrude(6)
        .translate((width / 2, 62, 0))
    )
    # テキストも生成
    text1_obj = __generate_text_model(text1, text_size, text_x, 28, text_tickness)
    text2_obj = __generate_text_model(text2, text_size, text_x, 18, text_tickness)

    # 結合
    obj_result = plate_result.union(ornament_obj).union(text1_obj).union(text2_obj)

    # export stl
    cq.exporters.export(
        obj_result, str(export_dir / f"plate-{icon_dxf_path.name}_{text1}_{text2}.stl")
    )

    return obj_result


def main():
    # ソックス
    sock_plate_1 = generate_holiday_plate(
        Path(__file__).parent / "icon-socks.dxf",
        "I WANT ...",
        "Present!",
    )
    show_object(sock_plate_1)

    # プレゼント1
    presentbox1_plate_1 = generate_holiday_plate(
        Path(__file__).parent / "icon-presentbox1.dxf",
        "Merry",
        "Christmas :)",
    )
    show_object(presentbox1_plate_1.translate((100, 0, 0)))

    # ツリー2
    christmastree2_plate_1 = generate_holiday_plate(
        Path(__file__).parent / "icon-christmastree2.dxf",
        "Happy",
        "Holiday !!!",
    )
    show_object(christmastree2_plate_1.translate((200, 0, 0)))

    # 雪だるま
    snowman_plate_1 = generate_holiday_plate(
        Path(__file__).parent / "icon-snowman.dxf",
        "Let's",
        "Party !!",
    )
    show_object(snowman_plate_1.translate((50, 100, 0)))

    # サンタ帽子
    santahat_plate_1 = generate_holiday_plate(
        Path(__file__).parent / "icon-santa-hat.dxf",
        "Merry",
        "Christmas !!",
    )

    show_object(santahat_plate_1.translate((150, 100, 0)))


if __name__ == "__main__":
    main()
