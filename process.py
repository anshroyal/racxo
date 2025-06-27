
from PIL import Image
import io

def remove_img(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    datas = image.getdata()
    new_data = []
    for item in datas:
        # Simple rule: make pixels white-ish transparent
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    
    output = io.BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()
