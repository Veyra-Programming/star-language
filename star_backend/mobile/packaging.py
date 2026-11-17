"""
Star Mobile Application Packaging & Distribution Container (.starmobile)
Authoritative Reference: STAR_MOBILE_RUNTIME.md (Section 7)
"""

import os
import json
import zipfile
import hashlib
import time
from typing import Dict, Any, List, Optional
from star_runtime.mobile.abi import MOBILE_ABI_VERSION, MOBILE_ABI_MAGIC
from star_engine.compiler import StarCompiler
from star_engine.parser import Parser
from star_engine.lexer import Lexer


class MobileBundleManifest:
    def __init__(
        self,
        name: str = "StarApp",
        version: str = "0.8.0",
        package_id: str = "org.starlang.app",
        entry: str = "main.star",
        orientation: str = "portrait",
        permissions: Optional[List[str]] = None,
        abi_version: int = MOBILE_ABI_VERSION,
        min_sdk_version: int = 1
    ):
        self.name = name
        self.version = version
        self.package_id = package_id
        self.entry = entry
        self.orientation = orientation
        self.permissions = permissions or ["vibrate", "storage"]
        self.abi_version = abi_version
        self.min_sdk_version = min_sdk_version
        self.created_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "package_id": self.package_id,
            "entry": self.entry,
            "orientation": self.orientation,
            "permissions": self.permissions,
            "abi_version": self.abi_version,
            "min_sdk_version": self.min_sdk_version,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MobileBundleManifest":
        m = cls(
            name=data.get("name", "StarApp"),
            version=data.get("version", "0.8.0"),
            package_id=data.get("package_id", "org.starlang.app"),
            entry=data.get("entry", "main.star"),
            orientation=data.get("orientation", "portrait"),
            permissions=data.get("permissions", ["vibrate", "storage"]),
            abi_version=data.get("abi_version", MOBILE_ABI_VERSION),
            min_sdk_version=data.get("min_sdk_version", 1)
        )
        m.created_at = data.get("created_at", time.time())
        return m


class MobileBundle:
    """
    In-memory representation of a loaded .starmobile bundle.
    """
    def __init__(
        self,
        manifest: MobileBundleManifest,
        bytecode_bytes: bytes,
        source_code: Optional[str] = None,
        checksum: str = ""
    ):
        self.manifest = manifest
        self.bytecode_bytes = bytecode_bytes
        self.source_code = source_code or ""
        self.checksum = checksum

    def verify_checksum(self) -> bool:
        computed = hashlib.sha256(self.bytecode_bytes).hexdigest()
        return self.checksum == "" or self.checksum == computed


class MobilePackager:
    """
    Compiles Star source code and packages it into a portable .starmobile archive container.
    """
    def __init__(self):
        pass

    def build_bundle(
        self,
        source_file: str,
        output_path: Optional[str] = None,
        manifest_override: Optional[MobileBundleManifest] = None
    ) -> str:
        if not os.path.exists(source_file):
            raise FileNotFoundError(f"Source file not found: '{source_file}'")

        with open(source_file, "r", encoding="utf-8") as f:
            source = f.read()

        # 1. Compile to Star Bytecode
        lexer = Lexer(source, filename=source_file)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename=source_file)
        program = parser.parse()
        compiler = StarCompiler(filename=source_file)
        compiled_module = compiler.compile(program)
        bytecode_bytes = compiled_module.serialize()
        bytecode_checksum = hashlib.sha256(bytecode_bytes).hexdigest()

        # 2. Build Manifest
        base_name = os.path.splitext(os.path.basename(source_file))[0]
        manifest = manifest_override or MobileBundleManifest(
            name=base_name.capitalize(),
            entry=os.path.basename(source_file),
            package_id=f"org.starlang.{base_name.lower()}"
        )

        # 3. Determine output path
        if not output_path:
            out_dir = os.path.join("build", "mobile")
            os.makedirs(out_dir, exist_ok=True)
            output_path = os.path.join(out_dir, f"{base_name}.starmobile")
        else:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # 4. Write zip package
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            # Manifest
            zf.writestr("manifest.json", json.dumps(manifest.to_dict(), indent=2))
            # Bytecode
            zf.writestr("app.starb", bytecode_bytes)
            # Source
            zf.writestr("src/main.star", source)
            # Checksums
            meta = {
                "magic": MOBILE_ABI_MAGIC.decode("latin1"),
                "abi_version": MOBILE_ABI_VERSION,
                "bytecode_sha256": bytecode_checksum
            }
            zf.writestr("metadata.json", json.dumps(meta, indent=2))

        return output_path

    def load_bundle(self, bundle_path: str) -> MobileBundle:
        if not os.path.exists(bundle_path):
            raise FileNotFoundError(f"Mobile bundle not found: '{bundle_path}'")

        with zipfile.ZipFile(bundle_path, "r") as zf:
            manifest_data = json.loads(zf.read("manifest.json").decode("utf-8"))
            manifest = MobileBundleManifest.from_dict(manifest_data)
            bytecode_bytes = zf.read("app.starb")
            source_code = zf.read("src/main.star").decode("utf-8") if "src/main.star" in zf.namelist() else ""
            meta_data = json.loads(zf.read("metadata.json").decode("utf-8")) if "metadata.json" in zf.namelist() else {}
            checksum = meta_data.get("bytecode_sha256", "")

        bundle = MobileBundle(
            manifest=manifest,
            bytecode_bytes=bytecode_bytes,
            source_code=source_code,
            checksum=checksum
        )
        return bundle
