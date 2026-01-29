from PIL import Image, ImageDraw, ImageFont
import os

def render_text_with_highlights(text, sensitive_words, output_image_path=None, font_path="simhei.ttf", font_size=20):
    """
    Renders text to an image, highlighting sensitive words.
    Returns the PIL Image object.
    If output_image_path is provided, saves the image to that path.
    """
    # Configuration
    margin = 20
    line_spacing = 5
    max_width = 800
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    highlight_color = (255, 255, 0) # Yellow

    # Try to load font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # Fallback to a common Chinese font path on Windows if simhei.ttf is not found directly
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", font_size)
        except IOError:
            print("Warning: Chinese font not found. Text might not render correctly.")
            font = ImageFont.load_default()

    # Create a dummy image to calculate text size
    dummy_img = Image.new('RGB', (100, 100))
    draw = ImageDraw.Draw(dummy_img)

    # Process text to find highlight segments
    # We will split the text into a list of (text_segment, is_highlighted)
    
    # Sort sensitive words by length desc to match longest first
    sensitive_words = sorted([w for w in sensitive_words if w.strip()], key=len, reverse=True)
    
    # Map indices to boolean (highlighted or not)
    if not text:
        text = " " # Handle empty text to avoid crashes
        
    is_highlighted = [False] * len(text)
    
    for word in sensitive_words:
        start = 0
        while True:
            idx = text.find(word, start)
            if idx == -1:
                break
            # Mark indices
            for i in range(idx, idx + len(word)):
                is_highlighted[i] = True
            start = idx + 1
            
    # Reconstruct segments
    current_segment_text = ""
    current_highlight_state = is_highlighted[0] if text else False
    
    processed_segments = [] # List of (text, highlighted)
    
    for i, char in enumerate(text):
        if is_highlighted[i] == current_highlight_state:
            current_segment_text += char
        else:
            processed_segments.append((current_segment_text, current_highlight_state))
            current_segment_text = char
            current_highlight_state = is_highlighted[i]
    processed_segments.append((current_segment_text, current_highlight_state))

    # Now calculate layout
    lines = []
    current_line = []
    current_line_width = 0
    
    for seg_text, highlighted in processed_segments:
        # We need to handle wrapping *within* segments
        # Iterate char by char to be safe for Chinese wrapping
        for char in seg_text:
            if char == '\n':
                lines.append(current_line)
                current_line = []
                current_line_width = 0
                continue
            
            # For special chars like \r, just skip or treat as space? 
            # OCR often returns \n for newlines. \r\n might exist.
            if char == '\r':
                continue
                
            char_width = draw.textlength(char, font=font)
            
            if current_line_width + char_width > max_width - 2 * margin:
                lines.append(current_line)
                current_line = []
                current_line_width = 0
            
            current_line.append((char, highlighted))
            current_line_width += char_width
            
    if current_line:
        lines.append(current_line)

    # Calculate total height
    # Using getbbox to estimate line height usually works
    try:
        left, top, right, bottom = font.getbbox("A")
        line_height = bottom - top + line_spacing
    except:
        # Fallback for default font or weird cases
        line_height = font_size + line_spacing
        
    total_height = margin * 2 + len(lines) * line_height
    # Ensure minimum height
    total_height = max(total_height, 100)

    # Create final image
    img = Image.new('RGB', (max_width, int(total_height)), bg_color)
    draw = ImageDraw.Draw(img)
    
    y = margin
    for line in lines:
        x = margin
        for char, highlighted in line:
            char_width = draw.textlength(char, font=font)
            if highlighted:
                # Draw highlight rectangle
                draw.rectangle([x, y, x + char_width, y + line_height - line_spacing], fill=highlight_color)
            
            draw.text((x, y), char, font=font, fill=text_color)
            x += char_width
        y += line_height
        
    if output_image_path:
        img.save(output_image_path)
        print(f"Generated highlighted image at {output_image_path}")
        
    return img
