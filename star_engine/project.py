"""
Star Language Project & Configuration Management
Authoritative Reference: STAR_ECOSYSTEM.md & STAR_DISTRIBUTION.md
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ProjectConfig:
    name: str
    version: str = "1.1.0"
    entry: str = "src/main.star"
    target: str = "universal"
    description: str = "A Star Application"
    language: str = "1.1"


TEMPLATES = {
    "cli": {
        "description": "High-performance command-line application",
        "target": "cli",
        "main": """use IO
use System

app MainApp
    IO.print("🌟 Welcome to Star CLI!")
    IO.print("Arguments: " + System.args())
end
""",
        "test": """use Testing

test "CLI Basic Output"
    Testing.assert_true(true)
end
"""
    },
    "web": {
        "description": "Reactive WebAssembly browser application",
        "target": "web",
        "main": """use UI
use Web

app WebApp
    state count = 0

    UI.column(
        UI.title("Star WebAssembly Application"),
        UI.text("State counter: " + count),
        UI.button("Click Me (+1)", function()
            count = count + 1
        end)
    )
end
""",
        "test": """use Testing

test "Web State Initial"
    Testing.assert_true(true)
end
"""
    },
    "desktop": {
        "description": "Native multi-window desktop application",
        "target": "desktop",
        "main": """use UI
use Desktop

app DesktopApp
    state title = "Star Desktop"

    UI.window(title, 800, 600,
        UI.column(
            UI.title("Native Desktop Window"),
            UI.card(
                UI.text("Running on macOS, Windows, or Linux with hardware rendering.")
            )
        )
    )
end
""",
        "test": """use Testing

test "Desktop Window Spec"
    Testing.assert_true(true)
end
"""
    },
    "android": {
        "description": "Native Android NDK application with JNI bridge",
        "target": "android",
        "main": """use UI
use Mobile

app AndroidApp
    state battery_level = Mobile.Battery.level()

    UI.safe_area(
        UI.app_bar("Star Android App"),
        UI.card(
            UI.text("Battery Level: " + battery_level + "%"),
            UI.button("Trigger Haptic", function()
                Mobile.Haptics.vibrate("medium")
            end)
        )
    )
end
""",
        "test": """use Testing

test "Android Battery Probe"
    Testing.assert_true(true)
end
"""
    },
    "ios": {
        "description": "Native Apple iOS application with Metal GPU bridge",
        "target": "ios",
        "main": """use UI
use Mobile

app iOSApp
    UI.safe_area(
        UI.app_bar("Star iOS App"),
        UI.card(
            UI.text("Rendered via Apple MetalKit GPU Pipeline"),
            UI.button("Sensors", function()
                Mobile.Haptics.vibrate("light")
            end)
        )
    )
end
""",
        "test": """use Testing

test "iOS Safe Area"
    Testing.assert_true(true)
end
"""
    },
    "universal": {
        "description": "Universal cross-platform application (Web, Desktop, Android, iOS)",
        "target": "universal",
        "main": """use UI
use Mobile

app UniversalApp
    state counter = 0
    state platform_name = "Universal ABI v1"

    UI.safe_area(
        UI.app_bar("Star Universal App"),
        UI.column(
            UI.card(
                UI.title("Write Once. Run Everywhere."),
                UI.text("Platform Target: " + platform_name),
                UI.text("Active Counter: " + counter),
                UI.row(
                    UI.button("Decrement (-1)", function()
                        counter = counter - 1
                        Mobile.Haptics.vibrate("light")
                    end),
                    UI.button("Increment (+1)", function()
                        counter = counter + 1
                        Mobile.Haptics.vibrate("medium")
                    end)
                )
            )
        )
    )
end
""",
        "test": """use Testing

test "Universal App State Increment"
    variable count = 0
    count = count + 1
    Testing.assert_equal(count, 1)
end
"""
    }
}


def create_project(project_name: str, template: str = "universal", target_dir: Optional[str] = None) -> str:
    if target_dir is None and (os.path.isdir(template) or "/" in template or "\\" in template or (template.lower() not in TEMPLATES and template != "universal")):
        target_dir = template
        template = "universal"
    base = target_dir or os.getcwd()
    proj_path = os.path.join(base, project_name)
    tmpl_key = template.lower() if template.lower() in TEMPLATES else "universal"
    tmpl = TEMPLATES[tmpl_key]

    os.makedirs(proj_path, exist_ok=True)
    os.makedirs(os.path.join(proj_path, "src"), exist_ok=True)
    os.makedirs(os.path.join(proj_path, "assets"), exist_ok=True)
    os.makedirs(os.path.join(proj_path, "tests"), exist_ok=True)
    os.makedirs(os.path.join(proj_path, "build"), exist_ok=True)

    # 1. Write star.toml
    toml_content = f"""[project]
name = "{project_name}"
version = "1.1.0"
entry = "src/main.star"
target = "{tmpl['target']}"
description = "{tmpl['description']}"

[star]
language = "1.1"

[dependencies]
"""
    with open(os.path.join(proj_path, "star.toml"), "w", encoding="utf-8") as f:
        f.write(toml_content)

    # 2. Write src/main.star
    with open(os.path.join(proj_path, "src", "main.star"), "w", encoding="utf-8") as f:
        f.write(tmpl["main"])

    # 3. Write tests/test_main.star
    with open(os.path.join(proj_path, "tests", "test_main.star"), "w", encoding="utf-8") as f:
        f.write(tmpl["test"])

    # 4. Write README.md
    readme_content = f"""# {project_name}

A Star Application ({tmpl_key.capitalize()} Target).

## 🚀 Getting Started

```bash
# Run application
star run

# Build for target
star build

# Run tests
star test

# Package project archive
star package
```
"""
    with open(os.path.join(proj_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 5. Write .gitignore
    gitignore_content = """build/
dist/
*.starb
*.starmobile
*.starpkg
*.lock.tmp
"""
    with open(os.path.join(proj_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)

    # 6. Generate initial star.lock
    from star_runtime.packages import PackageManager
    pm = PackageManager(proj_path)
    pm.install()

    return proj_path


def init_project(target_dir: Optional[str] = None) -> str:
    dir_path = target_dir or os.getcwd()
    name = os.path.basename(os.path.abspath(dir_path))
    toml_path = os.path.join(dir_path, "star.toml")

    if os.path.exists(toml_path):
        raise FileExistsError(f"star.toml already exists in '{dir_path}'.")

    toml_content = f"""[project]
name = "{name}"
version = "1.1.0"
entry = "src/main.star"
target = "universal"
description = "A Star Application"

[star]
language = "1.1"

[dependencies]
"""
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(toml_content)

    return toml_path


def load_project(dir_path: Optional[str] = None) -> Optional[ProjectConfig]:
    p_dir = dir_path or os.getcwd()
    toml_path = os.path.join(p_dir, "star.toml")
    if not os.path.exists(toml_path):
        return None

    with open(toml_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    name = "unnamed"
    version = "1.1.0"
    entry = "src/main.star"
    target = "universal"
    desc = "A Star Application"
    lang = "1.1"

    for line in lines:
        line = line.strip()
        if "=" in line:
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "name":
                name = v
            elif k == "version":
                version = v
            elif k == "entry":
                entry = v
            elif k == "target":
                target = v
            elif k == "description":
                desc = v
            elif k == "language":
                lang = v

    return ProjectConfig(name=name, version=version, entry=entry, target=target, description=desc, language=lang)
