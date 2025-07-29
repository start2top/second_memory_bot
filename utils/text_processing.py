from PIL import Image
import pytesseract

def extract_text_from_image(image_path: str) -> str:
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng+rus')  # если нужен русский
        return text.strip()
    except Exception as e:
        return f"OCR error: {str(e)}"
