import colorsys

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    elif len(hex_str) == 8:
        hex_str = hex_str[:6] # drop alpha
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)

def map_color_to_5palette(hex_str):
    try:
        r, g, b = hex_to_rgb(hex_str)
    except Exception:
        return '#000000'
    
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    # Brightness / Luminance
    lum = 0.299*r + 0.587*g + 0.114*b

    # Pure white
    if lum >= 253:
        return '#FFFFFF'
    # Light canvas / soft background
    if lum >= 225:
        return '#F3F3F5'
    # Subtle hairline border
    if lum >= 200 and s < 0.25:
        return '#E5E5E8'
    # Deep Black
    if lum <= 30:
        return '#000000'
    
    # Red / Rose / Crimson / Danger -> Burgundy #92243D
    # Hue in degrees: 0..360. Reds are 330..360 or 0..20
    h_deg = h * 360
    if (h_deg >= 335 or h_deg <= 20) and s > 0.3:
        return '#92243D'
    
    # Blue / Indigo / Navy hues (200..260)
    if 190 <= h_deg <= 260:
        if lum < 120:
            return '#202F63' # Navy
        elif lum >= 180:
            return '#F3F3F5' # Light soft blue surface -> Soft gray
        else:
            return '#202F63'
            
    # Muted secondary text
    if s < 0.2:
        if lum < 120:
            return '#333333'
        else:
            return '#555555'

    # Any remaining greens, yellows, ambers, purples:
    # If light, soft gray #F3F3F5
    if lum >= 180:
        return '#F3F3F5'
    # If medium/dark, map to Black #000000 (neutral) or Navy #202F63
    if lum < 100:
        return '#000000'
    return '#202F63'

# Test on a few sample hexes
for sample in ['#01281A', '#E2EDE6', '#BE123C', '#1E3A8A', '#EEF2FF', '#92400E', '#065F46', '#E0E7FF']:
    print(f"{sample} -> {map_color_to_5palette(sample)}")

