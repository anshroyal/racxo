
from PIL import Image
from rembg import remove 
import io

def remove_img(image_bytes):
    out_bytes = remove(image_bytes)
    return out_bytes
