from typing import Optional
import logging

logger=logging.getLogger(__name__)

class TextParser:
    """
    parser for extracting text from plain text files (.txt files).
    """

    def parse(self,file_path:str) -> Optional[str]:
        """
        Read text from a plain text file.
        Args:
            file_path:path to the text file
        Returns:
            Extracted text as a string,or None if parsing fails
        """
        try:
            with open(file_path,'r',encoding='utf-8')as file:
                text=file.read()

            logger.info(f"Successfully Parsed text file: {file_path}")
            return text.strip()
        except UnicodeDecodeError:
            # If UTF-8 fails, try with error handling
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                logger.warning(f"Parsed text file with encoding issues: {file_path}")
                return text.strip()
            except Exception as e:
                logger.error(f"Error parsing text file {file_path}: {str(e)}")
                return None
        except Exception as e:
            logger.error(f"Error parsing text file {file_path}: {str(e)}")
            return None