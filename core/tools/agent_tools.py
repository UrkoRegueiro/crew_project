from crewai_tools import BaseTool
from typing import Union, Tuple, Dict
from core.tools.functions import info_videos


class InformationTool(BaseTool):
    name: str = "Information tool"
    description: str = ("This tool is used to obtain information about videos on youtube.")

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
        
    def _run(self):
        results = info_videos()
        return results




