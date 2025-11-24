from typing import List
import logging

logger=logging.getLogger(__name__)

class TextSplitter:
    """
    simple text splitter that splits text into chunks.

    """
    def __init__(self,chunk_size:int=1000,chunk_overlap:int=200):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
    def split_text(self,text:str)->List[str]:
        if not text:
            return []
        chunks=[]
        start=0
        text_length=len(text)
        while start<text_length:
            ##calculate end position 
            end=start+self.chunk_size

            chunk=text[start:end]
            chunks.append(chunk.strip())

            start=end-self.chunk_overlap
            if start>=end:
                start=end
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks