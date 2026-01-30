import cv2
import numpy as np


def flood_fill_remove(img_bgra, x, y, tolerance=5):
    """
    Tıklanan noktadaki renge benzer alanları bulur
    ve bu alanların alpha kanalını 0 yapar.
    Orijinal resmi BOZMADAN kopya üzerinde çalışır.
    """

    # Güvenlik: boş resim gelirse
    if img_bgra is None or img_bgra.size == 0:
        return img_bgra

    h, w = img_bgra.shape[:2]

    # Orijinali bozmamak için kopya al
    result = img_bgra.copy()

    # FloodFill RGB üzerinde daha sağlıklı çalışır
    rgb = result[:, :, :3].copy()

    # OpenCV floodFill için maske (+2 zorunlu)
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Flood fill uygula
    cv2.floodFill(
        rgb,
        mask,
        seedPoint=(x, y),
        newVal=(255, 255, 255),
        loDiff=(tolerance, tolerance, tolerance),
        upDiff=(tolerance, tolerance, tolerance),
        flags=4
    )

    # Gerçek maske alanı
    fill_mask = mask[1:-1, 1:-1] == 1

    # Maske içindeki pikselleri şeffaf yap
    result[fill_mask, 3] = 0

    return result
