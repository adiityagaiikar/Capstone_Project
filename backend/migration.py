import os
import shutil
from pathlib import Path

base_dir = Path(r"c:\Users\adity\OneDrive\Desktop\Capstone\backend")
app_dir = base_dir / "app"

# Create directories
(app_dir / "api" / "routers").mkdir(parents=True, exist_ok=True)
(app_dir / "core").mkdir(parents=True, exist_ok=True)
(app_dir / "models").mkdir(parents=True, exist_ok=True)
(app_dir / "services").mkdir(parents=True, exist_ok=True)

# Move files
files_to_move = {
    "database.py": app_dir / "core" / "database.py",
    "security.py": app_dir / "core" / "security.py",
    "models.py": app_dir / "models" / "models.py",
    "schemas.py": app_dir / "models" / "schemas.py",
    "main.py": app_dir / "main.py"
}

for src, dst in files_to_move.items():
    src_path = base_dir / src
    if src_path.exists():
        shutil.move(str(src_path), str(dst))

# Move routers
routers_dir = base_dir / "routers"
if routers_dir.exists():
    for f in routers_dir.iterdir():
        if f.is_file():
            shutil.move(str(f), str(app_dir / "api" / "routers" / f.name))
    shutil.rmtree(str(routers_dir), ignore_errors=True)

print("Migration successful")
