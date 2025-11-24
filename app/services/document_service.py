import os
from typing import List,Optional
import logging

from ingestion.parsers.pdf_parser import PDFParser
from ingestion.parsers.docx_parser import DOCXParser
from ingestion.parsers.text_parser import TextParser
from ingestion.chunkers.text_splitter import TextSplitter

logger=logging.getLogger(__name__)

class DocumentService:
    """
    Service for processing documents-parsing and chunking
    """
    def __init__(self):

        """
        Initialize the document service with parsing and splitter
        """
        self.pdf_parser=PDFParser()
        self.docx_parser=DOCXParser()
        self.text_parser=TextParser()
        self.text_splitter=TextSplitter()

    def process_document(self,file_path: str) -> Optional[List[str]]:
        """
        it will take a file path and return a list of chunks of text based on the file type
        """
        file_extension=os.path.splitext(file_path)[1].lower()
        text=None
        if file_extension=='.pdf':
            text=self.pdf_parser.parse(file_path)
        elif file_extension=='.docx':
            text=self.docx_parser.parse(file_path)
        elif file_extension==".txt":
            text=self.text_parser.parse(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return None
        if not text:
            logger.error(f"Failed to parse file:{file_path}")
            return None
        
        ##split text into chunks
        chunks=self.text_splitter.split_text(text)

        logger.info(f"successfully processed document: {file_path} into {len(chunks)} chunks")
        return chunks

