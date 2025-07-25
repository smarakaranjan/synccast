"""
synccast
-------

Python SDK for interacting with the SyncCast real-time messaging system.

Provides:
- SDK-style access via: `from synccast import synccast`
- Global configuration placeholders (overridable via SDK methods)
- Version metadata for distribution tracking
"""

from typing import Optional

# ── Version Info ────────────────────────────────────────────────────────────────
from synccast._version import VERSION as __version__

# ── Core SDK Access ─────────────────────────────────────────────────────────────
from synccast.sdk import SyncCastSDK

# ── Global Config Placeholders ──────────────────────────────────────────────────
# These can be optionally set before SDK initialization, or configured dynamically.
app_id: Optional[str] = None
app_secret: Optional[str] = None
api_base: str = "https://synccast.socialroots-test.net"  # Default API base

# ── Singleton SDK Instance ──────────────────────────────────────────────────────
# This provides a ready-to-use global SDK object.
synccast = SyncCastSDK()

# ── Public API Exposure ─────────────────────────────────────────────────────────
__all__ = [
    "__version__",
    "app_id",
    "app_secret",
    "api_base",
    "synccast",
    "SyncCastSDK",
]
