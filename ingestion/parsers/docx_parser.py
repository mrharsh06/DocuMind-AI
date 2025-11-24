from typing import Optional
from docx import Document
import logging

logger=logging.get_Logger(__name__)

class DOCXParser:
    """
    Parser for extracting text from DOCX files.
    """
    def parse(self, file_path:str) -> Optional[str]:
        """
        Extract text from a DOCX files.

        Args:
            file_path:path to the DOCX file

        Returns:
            Extracted text as a string,or None if parsing fails
        """
        try:
            doc=Document(file_path)
            text=""

            for paragraph in doc.paragraphs:
                text+=paragraph.text +"\n"

            logger.info(f"Successfully Parsed DOCX file: {file_path}")
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing DOCX file: {file_path}:{str(e)}")
            return None

