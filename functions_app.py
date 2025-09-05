import flet as ft
import shutil
import os
import re
from datetime import datetime


# # Поиск файла в папке по фильтру text
# def found_file(text, path):
#     list_file = []
#     found_text = re.compile(text)
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if found_text.search(file):
#                 print(file)
#                 list_file.append(file)
#     return list_file


def copy_file(path, copy_path):
    if os.path.isfile(path):
        shutil.copy(path, copy_path)
    elif os.path.isdir(path):
        shutil.copytree(path, copy_path)


def del_file_dir(path):
    if os.path.isfile(path):
        os.remove(path)

    if os.path.isdir(path):
        shutil.rmtree(path)


def get_size_dir(path):
    full_size = 0
    for root, dirs, files in os.walk(path):
        for d in dirs:
            d_path = os.path.join(root, d)
            size = 0
            for subroot, subfolder, subfiles in os.walk(d_path):
                for f in subfiles:
                    f_path = os.path.join(subroot, f)
                    size += os.path.getsize(f_path)
            full_size += size

        for f in files:
            f_path = os.path.join(root, f)
            f_size = os.path.getsize(f_path)
            full_size += f_size

        break
    return full_size


def convert_size(size):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ', 'ПБ']
    for unit in units:
        if size < 1024:
            return f"{size} {unit}"
        size = round(size / 1024, 2)


# {'main\\f': Checkbox(n='content'), 'main\\folder1': Checkbox(n='content'), 'main\\folder1\\folder3': Checkbox(n='content')
checkbox_paths = {}


def make_panel(path, level=0, update_tree=None):
    controls = []
    for entry in os.scandir(path):
        if entry.is_dir():
            c = ft.Checkbox()

            pb_for_dir = ft.PopupMenuButton(
                content=ft.Text(" ⋮ ", size=15),
                items=[ft.PopupMenuItem(text="Копировать", on_click=lambda _, p=entry.path: (copy_file(p, f'{p}_copy'),
                                                                                             update_tree() if update_tree else None)),
                       ft.PopupMenuItem(text="Удалить", on_click=lambda _, p=entry.path: (del_file_dir(p),
                                                                                          update_tree() if update_tree else None))],
                menu_position=ft.PopupMenuPosition.UNDER
            )

            checkbox_paths[entry.path] = c
            controls.append(
                ft.ExpansionPanelList(
                    expanded_header_padding=0,
                    controls=[
                        ft.ExpansionPanel(
                            can_tap_header=True,
                            header=ft.Row(
                                controls=[
                                    ft.Row(
                                        scroll=ft.ScrollMode.AUTO,
                                        width=300,
                                        spacing=5,
                                        controls=[
                                            ft.Text(' ' * level),
                                            pb_for_dir,
                                            ft.Icon(ft.Icons.FOLDER),
                                            ft.Text(entry.name),
                                        ]
                                    ),
                                    ft.Container(
                                        content=ft.Text(convert_size(get_size_dir(entry.path))),
                                        alignment=ft.alignment.center,
                                        width=600
                                    ),
                                    ft.Container(
                                        content=ft.Text(datetime.fromtimestamp(os.path.getctime(entry.path)).date()),
                                        width=100,
                                    ),
                                    ft.Container(
                                        content=c,
                                        expand=True,
                                        alignment=ft.alignment.center_right
                                    )
                                ]
                            ),
                            content=ft.Column(make_panel(entry.path, level + 5, update_tree=update_tree))
                        )
                    ]
                )
            )
    for entry in os.scandir(path):
        if entry.is_file():
            c = ft.Checkbox()

            pb_for_file = ft.PopupMenuButton(
                content=ft.Text(" ⋮ ", size=15),
                items=[ft.PopupMenuItem(text="Копировать", on_click=lambda _, p=entry.path: (copy_file(p, f'{p}_copy'),
                                                                                             update_tree() if update_tree else None)),
                       ft.PopupMenuItem(text="Удалить", on_click=lambda _, p=entry.path: (del_file_dir(p),
                                                                                          update_tree() if update_tree else None))],
                menu_position=ft.PopupMenuPosition.UNDER
            )

            checkbox_paths[entry.path] = c
            controls.append(
                ft.Row(
                    controls=[
                        ft.Row(
                            scroll=ft.ScrollMode.AUTO,
                            width=300,
                            spacing=5,
                            controls=[
                                ft.Text(' ' * level),
                                pb_for_file,
                                ft.Icon(ft.Icons.ATTACH_FILE_SHARP),
                                ft.Text(entry.name),
                            ]
                        ),
                        ft.Container(
                            content=ft.Text(convert_size(os.path.getsize(entry.path))),
                            alignment=ft.alignment.center,
                            width=600,
                        ),
                        ft.Container(
                            content=ft.Text(datetime.fromtimestamp(os.path.getctime(entry.path)).date()),
                            width=100,
                        ),
                        ft.Container(
                            content=c,
                            expand=True,
                            alignment=ft.alignment.center_right,
                        ),
                        ft.Container(width=46)
                    ]
                )
            )


    return controls
