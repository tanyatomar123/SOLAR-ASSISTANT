import gradio as gr
import cv2
import numpy as np
from PIL import Image

# Custom CSS for branding
custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
h1 {
    color: #2a6496;
    text-align: center;
}
.footer {
    text-align: center;
    font-size: 0.8em;
    color: #555;
}
"""

def analyze_rooftop(image):
    try:
        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        roof_area = np.sum(edges > 0) / 1000
        panel_capacity_kw = round(roof_area * 0.15, 2)
        annual_energy_kwh = int(panel_capacity_kw * 1200)
        roi_years = round(10000 / annual_energy_kwh, 1)

        report = f"""
        ⚡ AI Solar Assistant Report:
        ----------------------------
        - Estimated Rooftop Area: ~{roof_area:.1f} sqm
        - Recommended Solar Capacity: {panel_capacity_kw} kW
        - Annual Energy Generation: {annual_energy_kwh} kWh
        - Payback Period: ~{roi_years} years
        ----------------------------
        Tip: For accurate results, use a top-down rooftop image.
        """
        return report
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Gradio Interface with Custom Theme
demo = gr.Interface(
    fn=analyze_rooftop,
    inputs=gr.Image(type="pil", label="Upload Rooftop Image"),
    outputs=gr.Textbox(label="Analysis Report", lines=10),
    title="🔆 AI Solar Assistant",
    description="**Upload a rooftop image to estimate solar panel potential.**",
    css=custom_css,
    theme=gr.themes.Soft(primary_hue="blue"),  # Modern theme
    examples=[
        ["flat_roof.jpg"],
        ["angled_roof.jpg"]
    ],
    allow_flagging="never"
)

# Add a footer
demo.footer = """
<p class="footer">Powered by OpenCV & Gradio | © 2024 AI Solar Assistant</p>
"""

demo.launch(share=True)
