from docx.shared import RGBColor
try:
    c = RGBColor(255, 255, 0)
    print(f"Str: {str(c)}")
    print(f"Dir: {dir(c)}")
    print(f"R: {c.r}")
except Exception as e:
    print(e)
