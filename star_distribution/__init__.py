"""
Star Production Distribution Subsystem
Authoritative Reference: STAR_DISTRIBUTION.md
"""

from star_distribution.manifest import DistributionManifest
from star_distribution.integrity import IntegrityManager, IntegrityError
from star_distribution.archive import ArchiveEngine
from star_distribution.extractor import SecureExtractor, SecurityViolationError
from star_distribution.path_manager import PathManager
from star_distribution.installer import ProductionInstaller
from star_distribution.updater import SelfUpdater
from star_distribution.builder import ProductionDistributionBuilder, SourceExclusionViolationError

__all__ = [
    "DistributionManifest",
    "IntegrityManager",
    "IntegrityError",
    "ArchiveEngine",
    "SecureExtractor",
    "SecurityViolationError",
    "PathManager",
    "ProductionInstaller",
    "SelfUpdater",
    "ProductionDistributionBuilder",
    "SourceExclusionViolationError"
]
