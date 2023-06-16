#!/usr/bin/env python3

# Derived from https://gitlab.gnome.org/World/Rust/gtk-rust-template/-/blob/e86986f26a1bb5bae0a0a770bacb739365cf2e4d/create-project.py # noqa
# © 2023 Bilal Elmoussaoui, Ivan Molodetskikh, Alejandro Domínguez,
# Julian Hofer, Adrien Plazas, Maximiliano Sandoval R, Dave Patrick Caberto

import subprocess
import shutil
from pathlib import Path


print("Welcome to the GNOME Typescript Template")
name = input("App Name (e.g. My Awesome App): ")
project_name = input("Project Name (e.g. my-awesome-app): ")
app_id = input(
    "Application ID (e.g. org.domain.MyAwesomeApp, see: "
    "https://developer.gnome.org/documentation/tutorials/application-id.html): "  # noqa
)

for segment in app_id.split(".")[:-1]:
    if "-" in segment:
        exit("App IDs should only contain the '-' "
             "character in the last segment.")

author = input("Author Name: ")
update_contact = input("Author Email: ")
repo_url = input("Repo URL: ")

app_path = "/" + "/".join(app_id.split("."))
project_dir = Path(__file__).parent / project_name

CURRENT_APP_ID = "org.example.TypescriptTemplate"
CURRENT_PROJECT_NAME = "gnome-typescript-template"
CURRENT_NAME = "Typescript Template"
CURRENT_AUTHOR = "Christopher Davis"
CURRENT_EMAIL = "christopherdavis@gnome.org"
CURRENT_APP_PATH = "/org/example/TypescriptTemplate"
CURRENT_REPO_URL = "https://gitlab.gnome.org/BrainBlasted/gnome-typescript-template"

if project_dir.is_dir():
    wanna_remove = ""
    while wanna_remove not in ["y", "n"]:
        wanna_remove = input(
            "Project already exists, do you want to remove it? [y/n] "
        ).lower()

    if wanna_remove == "y":
        shutil.rmtree(project_dir)
    else:
        exit()


items_to_copy = [
    Path("build-aux"),
    Path("data"),
    Path("po"),
    Path("src"),
    Path("types"),
    Path(".editorconfig"),
    Path(".gitignore"),
    Path(".gitlab-ci.yml"),
    Path(".eslintignore"),
    Path(".eslintrc.js"),
    Path("meson.build"),
    Path("package-lock.json"),
    Path("package.json"),
    Path("README.md"),
    Path("tsconfig.json"),
]

for item in items_to_copy:
    item_path = Path(item)
    if item_path.is_dir():
        shutil.copytree(item_path, project_dir / item)
    else:
        shutil.copyfile(item_path, project_dir / item)


files_with_content_to_rename = [
    Path("build-aux") / "flatpak" / "org.example.TypescriptTemplate.json",
    Path("data") / "icons" / "meson.build",
    Path("data") / "meson.build",
    Path("data") / "org.example.TypescriptTemplate.desktop.in",
    Path("data") / "org.example.TypescriptTemplate.gschema.xml",
    Path("data") / "org.example.TypescriptTemplate.metainfo.xml.in",
    Path("data") / "org.example.TypescriptTemplate.data.gresource.xml",
    Path("data") / "window.ui",
    Path("po") / "POTFILES.in",
    Path("po") / "meson.build",
    Path("src") / "main.ts",
    Path("src") / "meson.build",
    Path("src") / "org.example.TypescriptTemplate.src.gresource.xml",
    Path("src") / "window.ts",
    Path(".gitlab-ci.yml"),
    Path("meson.build"),
    Path("package-lock.json"),
    Path("package.json"),
]

for file in files_with_content_to_rename:
    current_path = project_dir / file

    with open(current_path, "r") as handle:
        content = handle.read()
        content = content.replace(CURRENT_REPO_URL, repo_url)
        content = content.replace(CURRENT_APP_ID, app_id)
        content = content.replace(CURRENT_APP_PATH, app_path)
        content = content.replace(CURRENT_PROJECT_NAME, project_name)
        content = content.replace(CURRENT_NAME, name)
        content = content.replace(CURRENT_AUTHOR, author)
        content = content.replace(CURRENT_EMAIL, update_contact)

    with open(current_path, "w") as handle:
        handle.write(content)

files_to_rename = [
    Path("build-aux") / "flatpak" / "org.example.TypescriptTemplate.json",
    Path("data") / "icons" / "hicolor" / "symbolic" / "apps" /
    "org.example.TypescriptTemplate-symbolic.svg",
    Path("data") / "icons" / "hicolor" / "scalable" /
    "apps" / "org.example.TypescriptTemplate.svg",
    Path("data") / "org.example.TypescriptTemplate.desktop.in",
    Path("data") / "org.example.TypescriptTemplate.gschema.xml",
    Path("data") / "org.example.TypescriptTemplate.metainfo.xml.in",
    Path("data") / "org.example.TypescriptTemplate.data.gresource.xml",
    Path("src") / "org.example.TypescriptTemplate.in",
    Path("src") / "org.example.TypescriptTemplate.src.gresource.xml",
]


for file in files_to_rename:
    current_path = project_dir / file
    new_path = project_dir / file.parent / \
        str(file.name).replace(CURRENT_APP_ID, app_id)
    shutil.move(current_path, new_path)


subprocess.call(["git", "init", "-b", "main"], cwd=project_dir)

subprocess.call(["git", "submodule", "add",
                 "-b", "nightly",
                 "--name", "gi-types",
                 "https://gitlab.gnome.org/BrainBlasted/gi-typescript-definitions",
                 "gi-types"], cwd=project_dir)

# Add all files and commit them
subprocess.call(["git", "add", "-A"], cwd=project_dir)
subprocess.call(
    ["git", "commit", "-m", "Initialize with the GNOME Typescript Template"],
    cwd=project_dir)
