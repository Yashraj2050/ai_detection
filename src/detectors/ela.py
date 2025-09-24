from PIL import Image, ImageChops, ImageEnhance
import io

def ela_image(pil_image: Image.Image, quality: int = 90, scale: int = 10) -> Image.Image:
    # Save at quality -> reload -> compute difference
    temp_io = io.BytesIO()
    pil_image.save(temp_io, format='JPEG', quality=quality)
    temp_io.seek(0)
    recompressed = Image.open(temp_io)
    ela = ImageChops.difference(pil_image.convert('RGB'), recompressed.convert('RGB'))
    extrema = ela.getextrema()
    max_diff = max(b for a,b in extrema)
    if max_diff == 0:
        max_diff = 1
    factor = scale * 255.0 / max_diff
    ela = ImageEnhance.Brightness(ela).enhance(factor)
    return ela