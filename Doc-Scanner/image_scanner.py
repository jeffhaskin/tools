# image_scanner.py
import cv2
import numpy as np
from PIL import Image

class DocumentScanner:
    def __init__(self):
        self.kernel = np.ones((5, 5), np.uint8)

    def scan_document(self, image_path):
        """
        Process an image to detect and correct document perspective
        """
        # Read the image
        orig_img = cv2.imread(image_path)
        if orig_img is None:
            raise ValueError("Could not read the image")

        # Create a copy for processing
        img = orig_img.copy()
        
        # Preprocess the image
        img = self._preprocess_image(img)
        
        # Detect document edges
        corners = self._detect_document_edges(img)
        
        # Get the corrected image
        scanned = self._perspective_transform(orig_img, corners)
        
        # Convert to PIL Image for compatibility with other modules
        return Image.fromarray(cv2.cvtColor(scanned, cv2.COLOR_BGR2RGB))

    def _preprocess_image(self, img):
        """
        Prepare image for edge detection
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        
        # Apply Morphological operations
        morph = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, self.kernel, iterations=3)
        
        # Apply Canny edge detection
        edges = cv2.Canny(morph, 0, 200)
        edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        
        return edges

    def _detect_document_edges(self, edges):
        """
        Detect the four corners of the document
        """
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
        # Get the largest contour
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        # Find the contour with four corners
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            if len(approx) == 4:
                return self._order_points(approx.reshape(4, 2))
        
        raise ValueError("Could not detect document corners")

    def _order_points(self, pts):
        """
        Order points in top-left, top-right, bottom-right, bottom-left order
        """
        rect = np.zeros((4, 2), dtype=np.float32)
        
        # Top-left will have smallest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Top-right will have smallest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect

    def _perspective_transform(self, image, corners):
        """
        Apply perspective transform to get top-down view
        """
        # Calculate dimensions
        width_a = np.sqrt(((corners[2][0] - corners[3][0]) ** 2) + ((corners[2][1] - corners[3][1]) ** 2))
        width_b = np.sqrt(((corners[1][0] - corners[0][0]) ** 2) + ((corners[1][1] - corners[0][1]) ** 2))
        max_width = max(int(width_a), int(width_b))

        height_a = np.sqrt(((corners[1][0] - corners[2][0]) ** 2) + ((corners[1][1] - corners[2][1]) ** 2))
        height_b = np.sqrt(((corners[0][0] - corners[3][0]) ** 2) + ((corners[0][1] - corners[3][1]) ** 2))
        max_height = max(int(height_a), int(height_b))

        # Define destination points
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype=np.float32)

        # Get transformation matrix and apply it
        matrix = cv2.getPerspectiveTransform(corners.astype(np.float32), dst)
        scanned = cv2.warpPerspective(image, matrix, (max_width, max_height))
        
        return scanned
