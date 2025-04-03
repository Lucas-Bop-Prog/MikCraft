import os
import uuid
import subprocess
import minecraft_launcher_lib
import flet as ft

def instalar_minecraft(version, minecraft_dir):
    if not os.path.exists(os.path.join(minecraft_dir, "versions", version)):
        print(f"Descargando Minecraft {version}...")
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_dir)
        print("Descarga completada.")
    else:
        print("Minecraft ya está instalado.")

def iniciar_minecraft(username, version, minecraft_dir):
    player_uuid = str(uuid.uuid4()).replace("-", "")
    options = {
        "username": username,
        "uuid": player_uuid,
        "token": player_uuid,
    }
    
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_dir, options)
    print("Iniciando Minecraft...")
    subprocess.run(minecraft_command)

def main(page: ft.Page):
    page.title = "Minecraft Launcher"
    page.window_width = 400
    page.window_height = 400
    
    profile_input = ft.TextField(label="Perfil de Minecraft", value="Default")
    
    username_input = ft.TextField(label="Nombre de usuario", value="Player")
    
    def update_versions():
        minecraft_dir = f"Profiles/{profile_input.value}"
        os.makedirs(minecraft_dir, exist_ok=True)
        versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_dir)
        return [version["id"] for version in versions]
    
    all_versions = update_versions()
    
    version_dropdown = ft.Dropdown(
        label="Versión de Minecraft",
        options=[ft.dropdown.Option(v) for v in all_versions],
        value=all_versions[0] if all_versions else "1.20.1"
    )
    
    search_input = ft.TextField(label="Buscar versión")
    
    def on_search_change(e):
        query = search_input.value.lower()
        filtered_versions = [v for v in all_versions if query in v]
        version_dropdown.options = [ft.dropdown.Option(v) for v in filtered_versions]
        version_dropdown.update()
    
    search_input.on_change = on_search_change
    
    def on_start_click(e):
        minecraft_dir = f"Profiles/{profile_input.value}"
        os.makedirs(minecraft_dir, exist_ok=True)
        username = username_input.value
        version = version_dropdown.value
        instalar_minecraft(version, minecraft_dir)
        iniciar_minecraft(username, version, minecraft_dir)
    
    start_button = ft.ElevatedButton("Iniciar Minecraft", on_click=on_start_click)
    
    page.add(profile_input, username_input, search_input, version_dropdown, start_button)

ft.app(target=main)
