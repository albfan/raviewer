"""Keeps track of items structure in application"""
import dearpygui.dearpygui as dpg

items = {
    "windows": {
        "viewport": dpg.generate_uuid(),
        "previewer": dpg.generate_uuid(),
        "settings": dpg.generate_uuid(),
        "hex_mode": dpg.generate_uuid(),
        "hex_tab": None,
    },
    "static_text": {
        "color_format": dpg.generate_uuid(),
        "color_description": dpg.generate_uuid(),
        "image_resolution": dpg.generate_uuid(),
    },
    "registries": {
        "texture_registry": dpg.generate_uuid(),
        "add_mouse_click_handler": dpg.generate_uuid(),
    },
    "buttons": {
        "read_file": dpg.generate_uuid(),
        "combo": dpg.generate_uuid(),
        "export_image": dpg.generate_uuid(),
        "width_setter": dpg.generate_uuid(),
        "height_setter": dpg.generate_uuid(),
        "color_picker": dpg.generate_uuid(),
        "anti_checkbox": dpg.generate_uuid(),
        "r_ychannel": dpg.generate_uuid(),
        "g_uchannel": dpg.generate_uuid(),
        "b_vchannel": dpg.generate_uuid(),
        "ychannel": dpg.generate_uuid(),
        "uchannel": dpg.generate_uuid(),
        "vchannel": dpg.generate_uuid(),
        "append_remove": dpg.generate_uuid(),
        "nnumber": dpg.generate_uuid(),
        "nvalues": dpg.generate_uuid(),
    },
    "menu_bar": {
        "export_tab": dpg.generate_uuid(),
        "file": dpg.generate_uuid(),
        "mode": dpg.generate_uuid(),
    },
    "texture": {
        "raw": None,
    },
    "plot": {
        "main_plot": dpg.generate_uuid(),
        "xaxis": dpg.generate_uuid(),
        "yaxis": dpg.generate_uuid(),
        "annotation": dpg.generate_uuid(),
        "tab": dpg.generate_uuid(),
    },
    "file_selector": {
        "read": dpg.generate_uuid(),
        "export": dpg.generate_uuid(),
        "export_image": dpg.generate_uuid(),
        "export_raw": dpg.generate_uuid(),
    },
}
