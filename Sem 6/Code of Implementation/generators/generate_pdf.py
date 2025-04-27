from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

# Register a font that supports Marathi (Unicode)
font_path = "frontend/assets/NotoSansDevanagari-Regular.ttf"  # Update if needed
pdfmetrics.registerFont(TTFont("NotoSansDevanagari", font_path))

# Load the background JPG template
background_image_path = "frontend/assets/pdf-output-template.jpg"  # Update with actual path
bg_reader = ImageReader(background_image_path)

def get_pdf(title, sentences, image_objects):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Define text formatting style (center-aligned)
    styles = getSampleStyleSheet()
    unicode_style = ParagraphStyle(
        "UnicodeStyle",
        parent=styles["Normal"],
        fontName="NotoSansDevanagari",
        fontSize=16,  # Increased font size
        leading=20,  # More spacing between lines
        alignment=1,  # **Center-aligned text**
    )

    first_page = True  # Flag to check if it's the first page

    for i, (sentence, image_object) in enumerate(zip(sentences, image_objects)):
        # **Don't call showPage() on the first iteration to avoid blank page**
        if not first_page:
            c.showPage()
        first_page = False  # Mark first page as processed

        c.drawImage(bg_reader, 0, 0, width=width, height=height)  # Draw background

        # Title on the first page only
        if i == 0:
            c.setFont("NotoSansDevanagari", 28)  # Bigger title
            c.setFillColorRGB(0.2, 0.2, 0.2)
            c.drawCentredString(width / 2, height - 100, title)

        y_position = height - 250  # Adjusted position for better layout

        # Draw the text (Centered)
        paragraph = Paragraph(sentence, unicode_style)
        text_width, text_height = paragraph.wrap(450, y_position)
        paragraph.drawOn(c, (width - text_width) / 2, y_position - text_height)  # Center the paragraph

        y_position -= text_height + 60  # More spacing between text and image

        # Draw the image, now **bigger**
        if image_object:
            pil_image = ImageReader(image_object)
            img_width = 5 * inch  # Increased width
            img_height = 4 * inch  # Increased height
            c.drawImage(pil_image, (width - img_width) / 2, y_position - img_height, width=img_width, height=img_height)
        else:
            c.setFont("Helvetica", 12)
            c.drawCentredString(width / 2, y_position - 20, "[Image Not Available]")

    c.save()
    buffer.seek(0)
    return buffer
