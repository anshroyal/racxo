from rembg import remove, new_session
from PIL import Image
import io

# Create a session with your local model
session = new_session(model_name="u2net", model_path="u2net.onnx")

def remove_img(image_bytes):
    out_bytes = remove(image_bytes, session=session)
    out_img = Image.open(io.BytesIO(out_bytes))
    return out_bytes
