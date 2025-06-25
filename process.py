from rembg import remove
from PIL import Image
import io

def remove_img(image_bytes):
    out_bytes = remove(image_bytes)
    out_img = Image.open(io.BytesIO(out_bytes))
    out_img.show()  # Optional: remove if running on server without display
    return out_bytes
