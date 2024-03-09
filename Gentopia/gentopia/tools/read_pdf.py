from gentopia.tools.basetool import *
from PyPDF2 import PdfReader
from typing import AnyStr
import requests
import io

class ReadPdfArgs(BaseModel):
    path: str = Field(..., description="path to the PDF or URL")

class ReadPdf(BaseTool):
    """Tool that reads a PDF file from path or url and returns the text."""

    name = "read_pdf"
    description = ("A tool that reads a PDF file from path or url and returns the text.")

    args_schema: Optional[Type[BaseModel]] = ReadPdfArgs

    def _run(self, path: AnyStr) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            response = requests.get(path)
            response.raise_for_status()
            file = io.BytesIO(response.content)
        else:
            with open(path, 'rb') as file:
                file = file.read()
        
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = ReadPdf()._run("../Transformer.pdf")
    print(ans)