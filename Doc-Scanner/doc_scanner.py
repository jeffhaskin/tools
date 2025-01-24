# main.py
import os
import sys
import argparse
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from document_processor import DocumentProcessor
from image_scanner import DocumentScanner
from ocr_handler import OCRHandler
from file_utils import get_desktop_path, ensure_directory

class DocumentScannerApp:
    def __init__(self):
        self.scanner = DocumentScanner()
        self.processor = DocumentProcessor()
        self.ocr = OCRHandler()

    def process_document(self, image_path, output_dir=None, base_name="processed_document", output_format="md"):
        """
        Process a document image and save the results.
        
        Args:
            image_path (str): Path to the input image
            output_dir (str, optional): Directory to save output files. Defaults to desktop.
            base_name (str, optional): Base name for output files. Defaults to "processed_document".
            output_format (str, optional): Output format for text document ('md' or 'docx'). Defaults to "md".
        
        Returns:
            tuple: Paths to the saved image and document files
        
        Raises:
            ValueError: If output_format is not 'md' or 'docx'
            RuntimeError: If processing fails
        """
        if output_format not in ['md', 'docx']:
            raise ValueError("output_format must be 'md' or 'docx'")

        # Set up output directory
        output_dir = Path(output_dir) if output_dir else get_desktop_path()
        ensure_directory(output_dir)

        try:
            # Process the image
            scanned_image = self.scanner.scan_document(image_path)
            
            # Save processed image
            image_output_path = output_dir / f"{base_name}.png"
            self.processor.save_image(scanned_image, image_output_path)
            
            # Perform OCR and save document
            text_content = self.ocr.process_image(scanned_image)
            doc_output_path = output_dir / f"{base_name}.{output_format}"
            self.processor.save_document(text_content, doc_output_path, output_format)
            
            return str(image_output_path), str(doc_output_path)

        except Exception as e:
            raise RuntimeError(f"Document processing failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Process document images and convert to text.')
    parser.add_argument('image_path', help='Path to the document image')
    parser.add_argument('--output_format', choices=['md', 'docx'], default='md',
                      help='Output format (md or docx)')
    parser.add_argument('--output_dir', type=str, help='Output directory path (default: desktop)')
    parser.add_argument('--base_name', type=str, default='processed_document',
                      help='Base name for output files (without extension)')

    args = parser.parse_args()

    app = DocumentScannerApp()
    
    try:
        print("Processing document...")
        image_path, doc_path = app.process_document(
            args.image_path,
            args.output_dir,
            args.base_name,
            args.output_format
        )
        print(f"Processed image saved to: {image_path}")
        print(f"Document saved to: {doc_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()