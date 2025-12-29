
import io
import qrcode
import pygame

def make_qr_surface(url: str, size_px: int = 240) -> pygame.Surface:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    surface = pygame.image.load(buf).convert_alpha()
    surface = pygame.transform.smoothscale(surface, (size_px, size_px))
    return surface
