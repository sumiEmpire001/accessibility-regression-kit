"""Create a downloadable static site, without bundlers or runtime dependencies."""
import shutil
from pathlib import Path
root = Path(__file__).parent
out = root / "dist"
out.mkdir(exist_ok=True)
for name in ("index.html", "styles.css", "TESTING.md"):
    shutil.copyfile(root / name, out / name)
print("Built dist/: open index.html after extracting the artifact")
