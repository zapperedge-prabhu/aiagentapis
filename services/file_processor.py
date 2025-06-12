import logging
import io
import PyPDF2
from typing import Tuple

logger = logging.getLogger(__name__)

class FileProcessor:
    """Handles processing of different file types to extract text content"""
    
    @staticmethod
    def extract_text_from_content(content: bytes, content_type: str = None, filename: str = None) -> str:
        """
        Extract text content from file bytes based on content type
        
        Args:
            content (bytes): File content as bytes
            content_type (str): MIME type of the file
            filename (str): Original filename for type detection
            
        Returns:
            str: Extracted text content
        """
        try:
            # Determine file type
            file_type = FileProcessor._determine_file_type(content_type, filename, content)
            
            if file_type == 'pdf':
                return FileProcessor._extract_from_pdf(content)
            elif file_type in ['txt', 'text']:
                return FileProcessor._extract_from_text(content)
            else:
                # Try to decode as text first
                try:
                    return FileProcessor._extract_from_text(content)
                except UnicodeDecodeError:
                    raise ValueError(f"Unsupported file type: {file_type}")
                    
        except Exception as e:
            logger.error(f"Error extracting text from file: {e}")
            raise

    @staticmethod
    def _determine_file_type(content_type: str, filename: str, content: bytes) -> str:
        """Determine file type from various indicators"""
        
        # Check content type
        if content_type:
            if 'pdf' in content_type.lower():
                return 'pdf'
            elif 'text' in content_type.lower():
                return 'text'
        
        # Check filename extension
        if filename:
            filename_lower = filename.lower()
            if filename_lower.endswith('.pdf'):
                return 'pdf'
            elif filename_lower.endswith(('.txt', '.md', '.csv', '.json', '.xml')):
                return 'text'
        
        # Check file signature (magic bytes)
        if content.startswith(b'%PDF'):
            return 'pdf'
        
        # Default to text
        return 'text'

    @staticmethod
    def _extract_from_pdf(content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                raise ValueError("PDF is encrypted and cannot be processed")
            
            text_content = []
            total_pages = len(pdf_reader.pages)
            
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text.strip():  # Only add non-empty pages
                    text_content.append(page_text)
            
            extracted_text = '\n'.join(text_content)
            
            if not extracted_text.strip():
                raise ValueError(
                    f"No extractable text found in PDF ({total_pages} pages). "
                    "This PDF might be image-based, scanned, or have text extraction restrictions. "
                    "Please try with a different PDF that contains selectable text."
                )
                
            logger.info(f"Successfully extracted text from PDF: {len(extracted_text)} characters from {total_pages} pages")
            return extracted_text
            
        except PyPDF2.errors.PdfReadError as e:
            logger.error(f"PDF read error: {e}")
            raise ValueError(f"Invalid or corrupted PDF file: {e}")
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")

    @staticmethod
    def _extract_from_text(content: bytes) -> str:
        """Extract text from text-based content"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    return content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            raise UnicodeDecodeError("Unable to decode content with any supported encoding")
            
        except Exception as e:
            logger.error(f"Error extracting text from text file: {e}")
            raise ValueError(f"Failed to extract text: {e}")

    @staticmethod
    def validate_text_length(text: str, max_length: int = 100000) -> Tuple[str, bool]:
        """
        Validate and potentially truncate text length for API limits
        
        Args:
            text (str): Text content to validate
            max_length (int): Maximum allowed length
            
        Returns:
            Tuple[str, bool]: (processed_text, was_truncated)
        """
        if len(text) <= max_length:
            return text, False
        
        logger.warning(f"Text length {len(text)} exceeds limit {max_length}, truncating")
        return text[:max_length], True
