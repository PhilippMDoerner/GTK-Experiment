#!/usr/bin/env python3

import sys
import os

def to_camel_case(s):
  if '-' in s:
    s.replace('-', '_')
  return ''.join(word.capitalize() for word in s.split('_'))

def write_file(path, content):
  with open(path, "w") as f:
    f.write(content)

def insert_line_after(filepath, marker_line, line_to_insert):
  with open(filepath, "r+") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
      if marker_line in line:
        lines.insert(i + 1, f"{line_to_insert}\n")
        break
    f.seek(0)
    f.writelines(lines)

if len(sys.argv) != 2:
    print("Usage: gen_widget.py <WidgetName>")
    sys.exit(1)

app_id = "org.example.TypescriptTemplate"
domain_prefix = '/'.join(app_id.split('.')) # Creates i.e. org/domain/mine from org.domain.mine
relative_path = sys.argv[1]
dir_path = f"src/{relative_path}"
name = os.path.basename(relative_path)  # Extract the last component of the path
class_name = to_camel_case(name)
meta_name = f"{class_name}Meta"
ui_filename = f"{name}.ui"
ts_filename = f"{name}.ts"
js_filename = f"{name}.js" # Exists after build step
os.makedirs(dir_path, exist_ok=True)

# Create .ui
default_ui_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <template class="{class_name}" parent="GtkBox">
    <child>
      <object class="GtkLabel">
        <property name="label">{class_name} works!</property>
      </object>
    </child>
  </template>
</interface>
""".strip()
write_file(f"{dir_path}/{ui_filename}", default_ui_template)

# Create .ts
default_ts_template = f"""
import Gtk from "gi://Gtk";
import {'{ TSWidget }'} from "src/widget_meta";

const {class_name} = class extends Gtk.Box {{}};

export const {meta_name}: TSWidget = {{
  template: "resource:///{domain_prefix}/{relative_path}/{ui_filename}",
  GTypeName: "{class_name}",
  klass: {class_name},
}}
""".strip()
write_file(f"{dir_path}/{ts_filename}", default_ts_template)

# Append to POTFILES.in
with open("po/POTFILES.in", "a") as f:
  f.write(f"{dir_path}/{ts_filename}\n")
  f.write(f"{dir_path}/{ui_filename}\n")

# Append to gresource.xml
gresource_file = f"src/{app_id}.src.gresource.xml"
ts_resource_line = f'<gresource prefix="/{domain_prefix}/js">'
ui_resource_line = f'<gresource prefix="/{domain_prefix}">'

insert_line_after(gresource_file, ts_resource_line, f'{4*' '}<file>{relative_path}/{js_filename}</file>')
insert_line_after(gresource_file, ui_resource_line, f'{4*' '}<file preprocess="xml-stripblanks">{relative_path}/{ui_filename}</file>')

# Append to src/meson.build
meson_file = "src/meson.build"
insert_line_after(meson_file, "sources = files", f"{2*' '}'{relative_path}/{ts_filename}',")

# Append to widget_registry.ts
widget_registry_file = "src/widget_registry.ts"
insert_line_after(widget_registry_file, "import GObject", f"import {'{ ' + meta_name + ' }'} from './{relative_path}/{js_filename}';")
insert_line_after(widget_registry_file, "const WIDGET_REGISTRY", f"{4*' '}{meta_name},")

print(f"Widget {name} created successfully.")
