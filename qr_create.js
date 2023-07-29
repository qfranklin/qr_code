const fs = require('fs');
const QRCode = require('qrcode-svg');

// Create a new QRCode instance with the desired data
const qrCode = new QRCode("https://github.com/qfranklin/qr_code");

// Generate the SVG representation of the QR code
const svgString = qrCode.svg();

// Save the SVG content to a file
fs.writeFileSync('input/qrcode_script.svg', svgString);

console.log('QR code saved as qrcode.svg');