const fs = require('fs');
const QRCode = require('qrcode-svg');

// URLs to generate QR codes for
const urls =  [
    "example_url"
];

// Loop through the URLs and generate QR codes
for (let i = 0; i < urls.length; i++) {
    const qrCode = new QRCode(urls[i]);
    const svgString = qrCode.svg();

    const fileName = `input/qrcode_${i + 1}.svg`;
    fs.writeFileSync(fileName, svgString);

    console.log(`QR code ${i + 1} saved as ${fileName}`);
}