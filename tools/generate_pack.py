from pathlib import Path
from PIL import Image, ImageDraw
import shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "Soft_Shader_Auto"
MAPS = OUT / "textures" / "colormap"
MAPS.mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "pack" / "manifest.json", OUT / "manifest.json")

def make_map(name, fn):
    im = Image.new("RGBA", (256, 256))
    px = im.load()
    for y in range(256):
        for x in range(256):
            px[x, y] = (*fn(x, y), 255)
    im.save(MAPS / name, optimize=True)

make_map("grass.png", lambda x,y: (int(145+24*x/255-10*y/255), int(177+18*x/255-5*y/255), int(126+12*x/255+8*y/255)))
make_map("foliage.png", lambda x,y: (int(126+22*x/255-7*y/255), int(165+20*x/255-6*y/255), int(112+12*x/255+8*y/255)))
make_map("water.png", lambda x,y: (int(100+15*x/255), int(166+20*x/255-6*y/255), int(190+18*x/255-4*y/255)))

icon = Image.new("RGB", (256,256), (190,218,194))
d = ImageDraw.Draw(icon)
d.ellipse((25,25,231,231), fill=(218,235,215))
d.polygon([(0,185),(75,105),(126,167),(178,92),(256,180),(256,256),(0,256)], fill=(111,155,119))
d.polygon([(0,213),(85,155),(142,205),(205,142),(256,190),(256,256),(0,256)], fill=(76,126,105))
d.ellipse((154,35,205,86), fill=(242,229,174))
d.rounded_rectangle((67,177,189,202), radius=12, fill=(231,242,224))
icon.save(OUT / "pack_icon.png", optimize=True)

(OUT / "README.txt").write_text("""SOFT SHADER - AUTO EDITION
Minecraft Bedrock 1.26.x

Install: open the .mcpack with Minecraft, then activate it in World Settings > Resource Packs.
No commands, cheats, behavior pack, or Vibrant Visuals toggle required.

This is a texture-based visual resource pack, not a GPU shader. It changes biome tint maps only.
It cannot add true real-time lighting, dynamic shadows, reflections, or bloom on standard Bedrock.
""", encoding="utf-8")

target = ROOT / "build" / "Soft-Shader-Auto.mcpack"
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for p in OUT.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(OUT).as_posix())
print(f"Built {target} ({target.stat().st_size} bytes)")
