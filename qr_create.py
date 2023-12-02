import qrcode
import qrcode.image.svg

# Your input data (e.g., a URL)
data = "Here is your present Samantha. -Q 12/1/23"

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,  # Adjust version as needed
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add the data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an SVG image factory
factory = qrcode.image.svg.SvgPathImage

# Generate the SVG QR code
svg_image = qr.make_image(image_factory=factory)

# Save the SVG QR code to a file
with open("input/qrcode.svg", "wb") as f:
    svg_image.save(f)
