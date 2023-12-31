# QR Code 3D Model Generator

This project creates a 3D model of a QR code by combining a JavaScript and Python script. It begins by generating an SVG representation of the QR code with JavaScript. Then, it uses Python to convert this SVG into a 3D model using the Blender library, and exports the model as an STL file. The Python script can also be used with the VSCode Blender extension for easier development and debugging.

## Dependencies

* Node.js (>=14.15.1)
* Python (>=3.6)
* npm (>=6.14.8)
* Blender (>=2.93)
* `qrcode-svg` npm package
* `bpy`, `mathutils`, `numpy`, `scipy` Python packages

## Installation

1. Clone the repository:

```bash
git clone https://github.com/qfranklin/qr_code.git
```

2. (Optional) If you want to use the VSCode Blender extension for development, install it from the [VSCode marketplace](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development).

## Usage

1. Generate the QR code SVG by running the Node.js script:

```bash
node qr_create.js
```

This will create a QR code SVG file for the URL "https://github.com/qfranklin/qr_code" and save it as `qrcode_script.svg` in the `input` directory.

2. Convert the QR code SVG to a 3D model using the Python script:

```bash
 "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" --background --python main.py
```

```bash
 exec(open("C:\\Users\\qfran\\Desktop\\code\\qr_code\\main.py").read())
```

This will create a 3D model from the SVG and save it as `file.stl` in the `output` directory.

3. Create the grid

```bash
 "C:\Users\qfran\AppData\Local\Programs\GIMP 2\bin\gimp-2.10.exe" -idf -b "(create_grid.py RUN-NONINTERACTIVE)" -b "(gimp-quit 0)"
```

Note: Please update the paths in the Python script according to your file system.

## Contributing

Please submit issues and pull requests for anything you'd like to contribute or any issues you find. We appreciate your help!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.