from typing import Optional
from PyPDF2 import PdfReader
import logging

logger=logging.getLogger(__name__)

class PDFParser:
    """
    Parser for extracting text from PDF files.
    """
    def parse(self, file_path:str) -> Optional[str]:
        """
        Extract text from a PDF files.

        Args:
            file_path:path to the PDF file

        Returns:
            Extracted text as a string,or None if parsing fails
        """
        try:
            reader=PdfReader(file_path)
            text=""

            #Extract text from each page
            for page in reader.pages:
                text+=page.extract_text() + "\n"

            logger.info(f"Successfully Parsed PDF file: {file_path}")
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing PDF file: {file_path}:{str(e)}")
            return None
