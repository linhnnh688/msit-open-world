"""Product image loading utilities.

The real pipeline feeds images directly to the MLLM backend. In this
reproduction the loader returns a PIL image when available and otherwise a
lightweight ImageRef descriptor so text-only backends (mock / GPT-4 text
fallback) can still reference the image slot.
"""

from dataclasses import dataclass
from typing import Optional, Union, Any


@dataclass
class ImageRef:
    """Serializable stand-in for a product image."""

    path: Optional[str] = None
    caption: str = "<product image>"

    def __repr__(self) -> str:  # keep logs concise
        return f"ImageRef(path={self.path!r})"


def load_image(path: Optional[str]) -> ImageRef:
    """Return an ImageRef for `path` (no PIL dependency required).

    When Pillow is installed and the file exists, `.as_pil()` can be used to
    obtain the actual pixels for vision backends.
    """
    return ImageRef(path=path)


def as_pil(image: ImageRef) -> Optional[Any]:
    """Best-effort conversion of an ImageRef to a PIL image (None if N/A)."""
    if image.path is None:
        return None
    try:
        from PIL import Image  # optional dependency

        return Image.open(image.path)
    except Exception:
        return None
