import flet as ft
import os
import re
from datetime import datetime

from functions_app import get_size_dir, make_panel, del_file_dir, checkbox_paths, convert_size


def main(page: ft.Page):
    page.title = 'Файловый менеджер'
    page.theme_mode = 'dark'
    page.scroll = "auto"

    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    panel = ft.Column()

    # Поиск файла в папке по фильтру text
    def found_file(e):
        text = dir_name.value
        list_file = []
        found_text = re.compile(text)
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if found_text.search(file):
                    print(file)
                    list_file.append(file)
        return list_file

    def update_tree():
        make_tree(None)
        page.update()

    #                                                     folder_name
    # full_path_dir - ...\project\\main\\folder1\\folder3': 'folder3', ...
    def make_tree(e):
        folder_name = dir_name.value
        full_path_dir = {}
        for root, dirs, files in os.walk(os.getcwd()):
            if folder_name in dirs:
                full_path_dir[os.path.join(root, folder_name)] = folder_name

        panel.controls = []

        for path, name in full_path_dir.items():
            panel.controls.append(
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
                                            ft.Text(name),
                                        ]
                                    ),
                                    ft.Container(
                                        content=ft.Text(convert_size(get_size_dir(path))),
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
            )
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

    def start(e):
        flag = False
        for root, dirs, files in os.walk(os.getcwd()):
            if dir_name.value in dirs:
                make_tree(e)
                btn_checkbox.visible = True
                flag = True
            elif dir_name.value in files:
                flag = True
                found_file(None)
                pass

        if not flag:
            error_found.value = f'Папка {dir_name.value} не найдена'
        else:
            error_found.value = ''
        page.update()

    table_title = ft.Row(
        controls=[
            ft.Container(content=ft.Text('Название файла'), width=570),
            ft.Container(content=ft.Text('Вес файла'), width=300),
            ft.Container(content=ft.Text('Дата создания файла'), width=450)
        ]
    )
    error_found = ft.Text("", color="red")
    dir_name = ft.TextField(label='Название папки', width=200, on_change=validate_btn_dir)
    btn_dir = ft.ElevatedButton('Выбрать', icon=ft.Icons.CHECK, width=200, disabled=True, on_click=start)
    btn_checkbox = ft.Container(
        content=ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, width=200, on_click=del_file_dir_checkbox,
                                  disabled=False),
        visible=False, alignment=ft.alignment.center_right
    )

    page.add(ft.Column([
        ft.Text('Введите название папки, в которой будет происходить поиск файлов'),
        dir_name,
        btn_dir,
        table_title,
        panel,
        btn_checkbox,
        error_found
    ]))


ft.app(target=main)
