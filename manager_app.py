import flet as ft
import os


def make_panel(path, level=0):
    controls = []
    for entry in os.scandir(path):
        if entry.is_dir():
            controls.append(
                ft.ExpansionPanelList(
                    elevation=8,
                    controls=[
                        ft.ExpansionPanel(
                            header=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.FOLDER),
                                    ft.Text(entry.name),
                                ]
                            ),
                            content=ft.Column(make_panel(entry.path, level + 1))
                        )
                    ]
                )
            )

    for entry in os.scandir(path):
        if entry.is_file():
            controls.append(
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ATTACH_FILE_SHARP),
                        ft.Text(entry.name)
                    ],
                    spacing=5
                )
            )
    return controls


def main(page: ft.Page):
    page.title = 'Файловый менеджер'
    page.theme_mode = 'dark'
    page.scroll = "auto"

    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def validate(e):
        if all([dir_name.value]):
            btn_dir.disabled = False
        else:
            btn_dir.disabled = True

        page.update()

    def write_to_main_txt(e):
        with open("main.txt", "w", encoding="utf-8") as f:
            f.write(dir_name.value)
        page.update()


    dir_name = ft.TextField(label='Название папки', width=200, on_change=validate)
    panel = ft.Column()

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

        panel.controls=[
            ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        header=ft.Text(folder_name),
                        content=ft.Column(make_panel(path))
                    )
                ]
            )
        ]

        page.update()

    btn_dir = ft.ElevatedButton('Выбрать', icon=ft.Icons.CHECK, width=200, disabled=True, on_click=make_tree)#on_click=write_to_main_txt, disabled=True)

    page.add(ft.Column([
        ft.Text('Введите название папки в которой будет происходить поиск файлов'),
        dir_name,
        btn_dir,
        panel
    ]))


ft.app(target=main)