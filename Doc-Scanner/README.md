### Manual use:

```shell
python doc_scanner.py scan.jpg --output_dir /path/to/output --base_name result
```

Both the markdown file and cropped and perspective-corrected photo will use the base name as the file name.

### Use it in a program:

```python
from document_scanner import DocumentScannerApp
from pathlib import Path

# Initialize scanner
scanner = DocumentScannerApp()

# Process a document
image_path, md_path = scanner.process_document(
    image_path="scan.jpg",
    output_dir="output",
    base_name="processed",
    output_format="md"
)

# Do something with the results
with open(md_path) as f:
    content = f.read()
print(content)
```

That processes a document and prints its text content. The process_document() function returns the paths to both the processed image and the text file.