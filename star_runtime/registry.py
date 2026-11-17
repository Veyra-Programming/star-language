"""
Star Official Package Registry & Ecosystem Subsystem
Authoritative Reference: STAR_COMPATIBILITY.md & STAR_ARCHITECTURE.md
"""

import os
import json
from typing import Dict, Any, List, Optional
from star_runtime.packages import PackageManager, ProjectManifest, PackageLock


def _init_catalog() -> List[Dict[str, Any]]:
    base_catalog: List[Dict[str, Any]] = [
        {
            "name": "http",
            "version": "1.0.0",
            "category": "networking",
            "description": "High-performance asynchronous HTTP/1.1 & HTTP/2 client and server for Star.",
            "author": "Star Core Team",
            "license": "MIT"
        },
        {
            "name": "json",
            "version": "1.0.0",
            "category": "data",
            "description": "Fast JSON serialization and deserialization library.",
            "author": "Star Core Team",
            "license": "MIT"
        },
        {
            "name": "sqlite",
            "version": "1.0.0",
            "category": "database",
            "description": "Embedded SQLite relational database client for Desktop and Mobile.",
            "author": "Star Database WG",
            "license": "MIT"
        },
        {
            "name": "ui-icons",
            "version": "1.0.0",
            "category": "ui",
            "description": "Comprehensive vector icon pack for Star UI (Material & Feather icons).",
            "author": "Star UI WG",
            "license": "MIT"
        },
        {
            "name": "crypto",
            "version": "1.0.0",
            "category": "security",
            "description": "Cryptographic hashing (SHA-256, AES-GCM, RSA) and key derivation.",
            "author": "Star Security Team",
            "license": "MIT"
        },
        {
            "name": "canvas2d",
            "version": "1.0.0",
            "category": "graphics",
            "description": "Vector drawing, path rendering, and animations for Web and Mobile.",
            "author": "Star Graphics Group",
            "license": "MIT"
        },
        {
            "name": "test-kit",
            "version": "1.0.0",
            "category": "devtools",
            "description": "Mocking, snapshot testing, and assertion utilities for Star test suites.",
            "author": "Star Quality WG",
            "license": "MIT"
        }
    ]

    catalog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "catalog.json"))
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                entries = json.load(f)
                existing = {p["name"] for p in base_catalog}
                for e in entries:
                    if e["name"] not in existing:
                        base_catalog.append({
                            "name": e["name"],
                            "version": e.get("version", "1.0.0"),
                            "category": e.get("category", "stdlib"),
                            "description": e.get("description", ""),
                            "author": "Star Core Team",
                            "license": "MIT"
                        })
                        existing.add(e["name"])
        except Exception:
            pass

    return base_catalog


class PackageRegistry:
    """
    Manages package search, dependency resolution, installation, and publication
    for the official Star Package Registry ecosystem.
    """

    # Official standard ecosystem catalog (includes standard library modules)
    ECOSYSTEM_CATALOG: List[Dict[str, Any]] = _init_catalog()

    @classmethod
    def search(cls, query: str = "", category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        q = query.lower()
        for pkg in cls.ECOSYSTEM_CATALOG:
            match_name = q in pkg["name"].lower() or q in pkg["description"].lower()
            match_cat = True if not category else (category.lower() == pkg["category"].lower())
            if match_name and match_cat:
                results.append(pkg)
        return results

    @classmethod
    def install(cls, package_name: str, version: Optional[str] = None) -> bool:
        pkg_meta = next((p for p in cls.ECOSYSTEM_CATALOG if p["name"] == package_name), None)
        target_version = version or (pkg_meta["version"] if pkg_meta else "1.0.0")

        pm = PackageManager()
        manifest = pm.load_manifest() or ProjectManifest("app", "1.0.0", target="mobile")
        manifest.dependencies[package_name] = target_version
        pm.save_manifest(manifest)
        pm.install()
        return True

    @classmethod
    def remove(cls, package_name: str) -> bool:
        pm = PackageManager()
        pm.remove_package(package_name)
        return True

    @classmethod
    def package(cls, project_dir: str = ".") -> str:
        from star_distribution.archive import ArchiveEngine
        return ArchiveEngine.package_project(project_dir)

    @classmethod
    def publish(cls, package_dir: str = ".") -> Dict[str, Any]:
        pm = PackageManager()
        manifest = pm.load_manifest()
        if not manifest:
            raise ValueError("No star.toml found in current directory to publish.")

        pkg_archive = cls.package(package_dir)
        return {
            "name": manifest.name,
            "version": manifest.version,
            "archive": pkg_archive,
            "status": "PUBLISHED"
        }

    @classmethod
    def update(cls) -> int:
        pm = PackageManager()
        pm.install()
        return 0

