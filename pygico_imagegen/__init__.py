"""PyGiCo-ImageGen: Python, GIMP, and ComfyUI based image generation and text addition tool."""

__version__ = "0.1.0"

from .content_analysis.blog_extractor import BlogExtractor
from .content_analysis.prompt_generator import PromptGenerator
from .image_generation.comfy_interface import ComfyInterface
from .image_processing.gimp_executor import GimpExecutor
from .utils.config_manager import ConfigManager

__all__ = [
    "BlogExtractor",
    "PromptGenerator",
    "ComfyInterface",
    "GimpExecutor",
    "ConfigManager",
]
