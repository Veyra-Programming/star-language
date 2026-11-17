import os
import zipfile
import hashlib
import shutil

def create_release_zip():
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
    src_dir = os.path.join(dist_dir, "Star-1.2.0-Windows-x64")
    zip_name = "Star-1.2.0-Windows-x64.zip"
    zip_path = os.path.join(dist_dir, zip_name)

    print(f"Creating zip from {src_dir} to {zip_path}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, src_dir)
                arcname = os.path.join("Star-1.2.0-Windows-x64", rel_p)
                zf.write(full_p, arcname)

    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    with open(zip_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
            sha512.update(chunk)

    sha256_hex = sha256.hexdigest()
    sha512_hex = sha512.hexdigest()

    with open(f"{zip_path}.sha256", "w", encoding="utf-8") as f:
        f.write(f"{sha256_hex}  {zip_name}\n")

    with open(f"{zip_path}.sha512", "w", encoding="utf-8") as f:
        f.write(f"{sha512_hex}  {zip_name}\n")

    portal_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web", "portal", "dist"))
    os.makedirs(portal_dist, exist_ok=True)
    shutil.copy2(zip_path, os.path.join(portal_dist, zip_name))

    print("ZIP CREATION SUCCESSFUL!")
    print(f"ZIP File:   {zip_path}")
    print(f"Size:       {os.path.getsize(zip_path)} bytes")
    print(f"SHA-256:    {sha256_hex}")
    print(f"SHA-512:    {sha512_hex}")
    return zip_path, sha256_hex, sha512_hex

if __name__ == "__main__":
    create_release_zip()
