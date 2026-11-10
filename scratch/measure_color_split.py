from PIL import Image
import numpy as np

def analyze_image_colors(image_path):
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    total_pixels = arr.shape[0] * arr.shape[1]
    
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    
    # Saturation spread
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    spread = max_c - min_c
    brightness = (r + g + b) // 3
    
    # Neutral criteria: low chroma, very bright (whites), or very dark (charcoals)
    # Slate/charcoal: r~41, g~53, b~46 -> spread ~12
    # Off-white: r~247, g~249, b~247 -> spread ~2
    # Border: r~225, g~233, b~227 -> spread ~8
    is_neutral = (spread < 28) | (brightness > 245) | (brightness < 30)
    
    # Brand green criteria: green noticeably higher than red & blue, and moderate to high saturation
    # Forest Green: #176B45 -> r:23, g:107, b:69 (g - r > 40, g - b > 15)
    # Soft Mint: #E8F3ED -> g highest but very bright, often counted in neutral/brand tint
    is_brand = (~is_neutral) & (g > r + 15) & (g >= b)
    
    # Accent criteria: warm orange, red, amber, yellow, or vivid non-green
    # Warm orange: #F28C28 -> r > g and r > b
    is_accent = (~is_neutral) & (~is_brand)
    
    neutral_count = np.sum(is_neutral)
    brand_count = np.sum(is_brand)
    accent_count = np.sum(is_accent)
    
    neutral_pct = round((neutral_count / total_pixels) * 100, 1)
    brand_pct = round((brand_count / total_pixels) * 100, 1)
    accent_pct = round((accent_count / total_pixels) * 100, 1)
    
    return {
        'neutral': neutral_pct,
        'brand': brand_pct,
        'accent': accent_pct
    }

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        res = analyze_image_colors(sys.argv[1])
        print(f"Neutral: {res['neutral']}%, Brand: {res['brand']}%, Accent: {res['accent']}%")

