# document_processor.py
from PIL import Image
from pathlib import Path
import python_docx_replace

class DocumentProcessor:
    def save_image(self, image, output_path):
        """
        Save the processed image
        
        Args:
            image: PIL Image object
            output_path: str, path where to save the image
        """
        try:
            # Ensure the output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save the image
            if isinstance(image, Image.Image):
                image.save(output_path, format='PNG')
            else:
                raise TypeError("Expected PIL Image object")
                
        except Exception as e:
            raise RuntimeError(f"Failed to save image: {str(e)}")

    def save_document(self, content, output_path, format_type):
        """
        Save the content as a document file
        
        Args:
            content: str, text content to save
            output_path: str, path where to save the document
            format_type: str, either 'md' or 'docx'
        """
        try:
            # Ensure the output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            if format_type == 'md':
                self._save_markdown(content, output_path)
            elif format_type == 'docx':
                self._save_docx(content, output_path)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
                
        except Exception as e:
            raise RuntimeError(f"Failed to save document: {str(e)}")

    def _save_markdown(self, content, output_path):
        """Save content as markdown file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _save_docx(self, content, output_path):
        """Save content as docx file"""
        from docx import Document
        
        doc = Document()
        for paragraph in content.split('\n'):
            if paragraph.strip():  # Skip empty lines
                doc.add_paragraph(paragraph)
        
        doc.save(output_path)
