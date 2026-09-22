"""GPT-4 backend (paper uses GPT-4 to construct AGTD/CTTD, Section 3.1/3.2).

Requires the `openai` package and OPENAI_API_KEY. Kept separate from the
core pipeline so the reproduction runs without network access.
"""

from typing import Any, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


class GPT4Backend:
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        if OpenAI is None:
            raise ImportError("Install the 'openai' package to use GPT4Backend.")
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = model

    def _encode_image(self, image: Any) -> Optional[dict]:
        """Encode a PIL image / path as an OpenAI image_url content part."""
        import base64
        import io
        import os

        if image is None:
            return None
        if isinstance(image, str) and os.path.exists(image):
            with open(image, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
        if hasattr(image, "save"):  # PIL image
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
        return None

    def generate(
        self,
        prompt: str,
        image: Optional[Any] = None,
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_new_tokens: int = 512,
    ) -> str:
        content = [{"type": "text", "text": prompt}]
        img = self._encode_image(image)
        if img is not None:
            content.append(img)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_new_tokens,
        )
        return resp.choices[0].message.content or ""
