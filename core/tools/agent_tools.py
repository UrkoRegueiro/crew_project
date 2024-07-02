from crewai_tools import BaseTool
from typing import Union, Tuple, Dict
from core.tools.functions import info_videos, send_email


class InformationTool(BaseTool):
    name: str = "Information tool"
    description: str = ("This tool is used to obtain information about videos on youtube.")

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
        
    def _run(self):
        results = info_videos()
        return results

class SenderTool(BaseTool):
    name: str = "Sender tool"
    description: str = ("This tool is used to send an email to all of the newspaper suscribers. The input variable 'text' is the final answer provided by the Newspaper Editor.")

    def _run(self, text: str):
        send_email(text)
        return "Emails sent."



