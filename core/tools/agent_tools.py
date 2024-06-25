from crewai_tools import BaseTool
from typing import Union, Tuple, Dict
from core.tools.functions import search_videos

class ScraperTool(BaseTool):
    name: str = "Sraper tool"
    description: str = ("Use this tool just once to gather information from youtube videos.")

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
        
    def _run(self):
        results = search_videos()
        return results



