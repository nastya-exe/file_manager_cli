import flet as ft
import os
from datetime import datetime

from functions_app import get_size_dir, make_panel, del_file_dir, checkbox_paths, convert_size


def main(page: ft.Page):
    page.title = 'Файловый менеджер'
    page.theme_mode = 'dark'
    page.scroll = "auto"

    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    panel = ft.Column()

    def update_tree():
        make_tree(None)
        page.update()

    def make_tree(e):
        folder_name = dir_name.value
        path = None

        with open('main.txt', 'r', encoding='utf-8') as f:
            name_main_dir = f.read()

        if folder_name == name_main_dir:
            path = name_main_dir
        else:
            for root, dirs, files in os.walk(name_main_dir):
                if folder_name in dirs:
                    path = os.path.join(root, folder_name)
                    break

        panel.controls = [
            ft.ExpansionPanelList(
                expanded_header_padding=0,
                controls=[
                    ft.ExpansionPanel(
                        can_tap_header=True,
                        expanded=True,
                        header=ft.Row(
                            controls=[
                                ft.Row(
                                    scroll=ft.ScrollMode.AUTO,
                                    width=300,
                                    spacing=5,
                                    controls=[
                                        ft.Icon(ft.Icons.FOLDER),
                                        ft.Text(folder_name),
                                    ]
                                ),
                                ft.Container(
                                    content=ft.Text(convert_size(get_size_dir(folder_name))),
                                    alignment=ft.alignment.center,
                                    width=600,
                                ),
                                ft.Container(
                                    content=ft.Text(datetime.fromtimestamp(os.path.getctime(path)).date()),
                                    width=100,
                                ),
                            ]
                        ),
                        content=ft.Column(make_panel(path, update_tree=update_tree))
                    )
                ]
            )
        ]
        page.update()

    def del_file_dir_checkbox(e):
        for item in checkbox_paths.items():
            if item[1].value:
                del_file_dir(item[0])
        make_tree(e)
        page.update()

    def validate_btn_dir(e):
        if all([dir_name.value]):
            btn_dir.disabled = False
        else:
            btn_dir.disabled = True
        page.update()

    def validate_btn_checkbox(e):
        pass


    def write_to_main_txt(e):
        with open("main.txt", "w", encoding="utf-8") as f:
            f.write(dir_name.value)
        make_tree(e)
        btn_checkbox.visible = True
        page.update()

    table_title = ft.Row(
        controls=[
            ft.Container(content=ft.Text('Название файла'), width=570),
            ft.Container(content=ft.Text('Вес файла'), width=300),
            ft.Container(content=ft.Text('Дата создания файла'), width=450)
        ]
    )

    dir_name = ft.TextField(label='Название папки', width=200, on_change=validate_btn_dir)
    btn_dir = ft.ElevatedButton('Выбрать', icon=ft.Icons.CHECK, width=200, disabled=True, on_click=write_to_main_txt)
    btn_checkbox = ft.Container(
        content=ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, width=200, on_click=del_file_dir_checkbox, disabled=False),
        visible=False, alignment=ft.alignment.center_right
    )

    page.add(ft.Column([
        ft.Text('Введите название директории, в которой будет происходить поиск файлов'),
        dir_name,
        btn_dir,
        table_title,
        panel,
        btn_checkbox,
    ]))


ft.app(target=main)
