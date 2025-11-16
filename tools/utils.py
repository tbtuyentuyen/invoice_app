""" Utilities Module """


import json
from pydotdict import DotDict
from PIL import Image as PILImage
from openpyxl.drawing.image import Image
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.utils import get_column_letter, column_index_from_string

PX_TO_EMU = 9525


def load_json(path: str) -> dict:
    """ Load json data"""
    with open(path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return DotDict(data)

def save_json(data: dict, path: str) -> None:
    """ Save json file """
    with open(path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

def _get_range_pixel_size(ws, start_cell: str, end_cell: str):
    """Get total pixel width/height for a cell range (handles merged cells)."""
    start_col = ''.join([c for c in start_cell if c.isalpha()])
    start_row = int(''.join([c for c in start_cell if c.isdigit()]))
    end_col = ''.join([c for c in end_cell if c.isalpha()])
    end_row = int(''.join([c for c in end_cell if c.isdigit()]))

    total_width = 0
    for col in range(column_index_from_string(start_col), column_index_from_string(end_col) + 1):
        total_width += (ws.column_dimensions[get_column_letter(col)].width or 8.43) * 7

    total_height = 0
    for row in range(start_row, end_row + 1):
        total_height += (ws.row_dimensions[row].height or 15) * 96 / 72

    return total_width, total_height

def add_image_fit_cell(ws, path: str, start_cell: str, end_cell: str = None, fit_inside=True):
    """
    Insert an image resized to fit inside a single cell or a merged cell range,
    centered within that area.
    """
    start_col_letter = ''.join([c for c in start_cell if c.isalpha()])
    start_row_idx = int(''.join([c for c in start_cell if c.isdigit()]))
    if end_cell is None:
        end_cell = start_cell

    # your helper should return total area in pixels for the range
    cell_w, cell_h = _get_range_pixel_size(ws, start_cell, end_cell)

    with PILImage.open(path) as im:
        img_w, img_h = im.size

    scale_w = cell_w / img_w if img_w else 1
    scale_h = cell_h / img_h if img_h else 1
    scale = min(scale_w, scale_h) if fit_inside else max(scale_w, scale_h)

    new_w = img_w * scale
    new_h = img_h * scale

    offset_x_px = max(0, (cell_w - new_w) / 2)
    offset_y_px = max(0, (cell_h - new_h) / 2)

    img = Image(path)
    img.width = new_w
    img.height = new_h

    col_idx = column_index_from_string(start_col_letter)
    marker = AnchorMarker(
        col=col_idx - 1,
        colOff=int(offset_x_px * PX_TO_EMU),
        row=start_row_idx - 1,
        rowOff=int(offset_y_px * PX_TO_EMU),
    )
    ext = XDRPositiveSize2D(cx=int(new_w * PX_TO_EMU), cy=int(new_h * PX_TO_EMU))
    img.anchor = OneCellAnchor(_from=marker, ext=ext)

    ws.add_image(img)

def clear_format_money(text: str):
    """ Clear format money """
    return text.replace('.', '').replace(',', '').replace('VNĐ', '').replace(' ', '').strip()
