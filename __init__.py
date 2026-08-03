from .nodes import MiniMaxH3HybridExtension
from .model_base_patch import install_hybrid_payload_patch

install_hybrid_payload_patch()

__all__ = ["MiniMaxH3HybridExtension"]

async def comfy_entrypoint():
    return MiniMaxH3HybridExtension()
