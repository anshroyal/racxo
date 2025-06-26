from rembg import remove, new_session
from PIL import Image
import io

session = new_session(model_name="u2netp")

def remove_img(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGBA")
    img.thumbnail((512, 512))  # Resize to reduce memory usage

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    out_bytes = remove(buf.read(), session=session)
    return out_bytes

