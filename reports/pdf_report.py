from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def generate_report(csv_path):

    df = pd.read_csv(csv_path)

    pdf = SimpleDocTemplate(
        "outputs/vehicle_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Vehicle Tracking Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Total Records: {len(df)}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Average Speed: {df['speed'].mean():.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Maximum Speed: {df['speed'].max():.2f}",
            styles["Normal"]
        )
    )

    pdf.build(content)