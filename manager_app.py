import flet as ft
import os
from datetime import datetime

from functions_app import get_size_dir, make_panel, del_file_dir, checkbox_paths, convert_size, get_file
from structure import add_structure


def main(page: ft.Page):
    page.title = 'Файловый менеджер'
    page.theme_mode = 'dark'
    page.scroll = "auto"

    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    panel = ft.Column()

    def found_file(e):
        panel.controls.clear()
        table_title.visible = True
        file_controls = get_file(os.getcwd(), dir_name.value, found_file=lambda e=None: found_file(e))
        panel.controls.extend(file_controls)
        if panel.controls:
            btn_checkbox.visible = True
            error_found.value = ''
        else:
            btn_checkbox.visible = False
            error_found.value = f'Файл или папка:  {dir_name.value} не найдены'
        page.update()

    def update_tree():
        make_tree(None)
        page.update()

    #                                                     folder_name
    # full_path_dir - ...\project\\main\\folder1\\folder3': 'folder3', ...
    def make_tree(e):
        checkbox_paths.clear()
        table_title.visible = True
        error_found.value = ''
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
                                        content=ft.Text(
                                            datetime.fromtimestamp(os.path.getctime(path)).strftime("%d.%m.%Y")),
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
        flag_dir = False
        for root, dirs, files in os.walk(os.getcwd()):
            if dir_name.value in dirs:
                make_tree(e)
                btn_checkbox.visible = True
                flag_dir = True

        if not flag_dir:
            found_file(None)

        page.update()

    def validate_btn_str(e):
        if add_str.value:
            btn_str.disabled = False
        page.update()

    def add_struct(e):
        add_structure(add_str.value)
        page.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            dir_name.value = e.files[0].name
            dir_name.update()

            start_pick_files(file_path)

    def start_pick_files(file_path):
        panel.controls.clear()
        table_title.visible = True

        if os.path.exists(file_path):
            file = get_file(
                os.path.dirname(file_path),
                os.path.basename(file_path),
                found_file=lambda e=None: start_pick_files(file_path)
            )
            panel.controls.extend(file)
            btn_checkbox.visible = True
        else:
            btn_checkbox.visible = False
            error_found.value = f'Файл "{os.path.basename(file_path)}" не найден'

        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    table_title = ft.Row(
        visible=False,
        controls=[
            ft.Container(content=ft.Text('Название файла'), width=570),
            ft.Container(content=ft.Text('Вес файла'), width=300),
            ft.Container(content=ft.Text('Дата создания файла'), width=450)
        ]
    )
    error_found = ft.Text("", color="red")
    dir_name = ft.TextField(label='Папка или файл', width=200, on_change=validate_btn_dir)
    add_str = ft.TextField(label='Название', width=200, on_change=validate_btn_str)

    btn_dir = ft.ElevatedButton('Выбрать', icon=ft.Icons.CHECK, width=200, disabled=True, on_click=start)
    btn_str = ft.ElevatedButton('Добавить', icon=ft.Icons.CHECK, width=200, disabled=True, on_click=add_struct)
    btn_pik = ft.ElevatedButton("Pick files", icon=ft.Icons.UPLOAD_FILE,
                                on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True))
    btn_checkbox = ft.Container(
        content=ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, width=200, on_click=del_file_dir_checkbox,
                                  disabled=False),
        visible=False, alignment=ft.alignment.center_right
    )

    page.add(ft.Column([
        ft.Row(
            spacing=148,
            controls=[
                ft.Text('Введите название папки, либо название файла (можно частично)'),
                ft.Text('Создать тестовую структуру папок')
            ]
        ),
        ft.Row(
            spacing=283,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        dir_name,
                        btn_pik
                    ]
                ),
                ft.Row(
                    controls=[
                        selected_files,
                        add_str
                    ]
                )
            ]
        ),
        ft.Row(
            spacing=400,
            controls=[
                btn_dir,
                btn_str
            ]
        ),
        table_title,
        panel,
        btn_checkbox,
        error_found
    ]))


ft.app(target=main)
