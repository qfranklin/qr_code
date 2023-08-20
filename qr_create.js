const fs = require('fs');
const QRCode = require('qrcode-svg');

// URLs to generate QR codes for
const urls = [
];

// Loop through the URLs and generate QR codes
for (let i = 0; i < urls.length; i++) {
    const qrCode = new QRCode(urls[i]);
    const svgString = qrCode.svg();

    const fileName = `input/qrcode_${i + 1}.svg`; // Generates filenames like "qrcode_1.svg", "qrcode_2.svg", etc.
    fs.writeFileSync(fileName, svgString);

    console.log(`QR code ${i + 1} saved as ${fileName}`);
}