import subprocess
import json
import tempfile
from pathlib import Path

class OCRHandler:
    def process_image(self, image):
        """
        Process an image using Surya OCR and return the text content
        
        Args:
            image: PIL Image object
        Returns:
            str: Extracted text content
        """
        try:
            # Save the PIL image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                image.save(tmp.name)
                temp_path = tmp.name

            # Create a temporary directory for results
            with tempfile.TemporaryDirectory() as temp_dir:
                # Run surya_ocr command line tool
                result = subprocess.run(
                    ['surya_ocr', temp_path, '--output_dir', temp_dir],
                    capture_output=True,
                    text=True,
                    check=True  # This will raise CalledProcessError if the command fails
                )

                # The results file will be in a subdirectory named after the input file
                base_name = Path(temp_path).stem
                results_dir = Path(temp_dir) / base_name
                results_file = results_dir / 'results.json'

                if not results_file.exists():
                    raise RuntimeError(f"Results file not found at {results_file}")

                with open(results_file) as f:
                    ocr_results = json.load(f)

                # Extract text from results
                # The results will be keyed by the temp filename without extension
                key = Path(temp_path).stem
                if key not in ocr_results:
                    raise ValueError(f"No results found for key {key} in output")

                # Get text lines from the first page
                text_lines = []
                for page in ocr_results[key]:
                    for line in page['text_lines']:
                        # Get the y-coordinate of the top of the text line's bounding box
                        y_position = line['bbox'][1]
                        text = line['text'].strip()
                        if text:  # Only include non-empty lines
                            text_lines.append((y_position, text))

                # Sort by vertical position and join text
                text_lines.sort(key=lambda x: x[0])
                return "\n".join(line[1] for line in text_lines)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"surya_ocr command failed: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {str(e)}")
        finally:
            # Clean up the temporary image file
            try:
                Path(temp_path).unlink()
            except:
                pass