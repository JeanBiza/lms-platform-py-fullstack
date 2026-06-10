from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def generate_certificate(user_name, course_name, date):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # borde decorativo
    c.setStrokeColorRGB(0.2, 0.4, 0.6)
    c.setLineWidth(3)
    c.rect(40, 40, width - 80, height - 80)

    c.setFont("Helvetica-Bold", 28)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.drawCentredString(width / 2, height - 150, "Certificate of Completion")

    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(width / 2, height - 220, "This certifies that")

    c.setFont("Helvetica-Bold", 20)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(width / 2, height - 260, user_name)

    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(width / 2, height - 300, "has successfully completed the course")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.drawCentredString(width / 2, height - 340, course_name)

    c.setFont("Helvetica-Oblique", 12)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(width / 2, height - 390, f"Issued on {date}")

    c.save()
    buffer.seek(0)
    return buffer