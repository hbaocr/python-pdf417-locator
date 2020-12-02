const fs = require('fs');
const jpeg = require('jpeg-js');



const {BarcodeFormat,
    MultiFormatReader,
    ZXingStringEncoding,
    PDF417DecodedBitStreamParser,
    DecodeHintType,
    RGBLuminanceSource, 
    BinaryBitmap, 
    HybridBinarizer} = require('@zxing/library')

const hints = new Map();
const formats = [BarcodeFormat.PDF_417];
hints.set(DecodeHintType.POSSIBLE_FORMATS, formats);
hints.set(DecodeHintType.TRY_HARDER, true);

const reader = new MultiFormatReader();
reader.setHints(hints);


const jpegData = fs.readFileSync('c0.jpg');
const rawImageData = jpeg.decode(jpegData);

const len = rawImageData.width * rawImageData.height;

const luminancesUint8Array = new Uint8Array(len);

for(let i = 0; i < len; i++){
	luminancesUint8Array[i] = ((rawImageData.data[i*4]+rawImageData.data[i*4+1]*2+rawImageData.data[i*4+2]) / 4) & 0xFF;
}

const luminanceSource = new RGBLuminanceSource(luminancesUint8Array, rawImageData.width, rawImageData.height);

console.log(luminanceSource)

const binaryBitmap = new BinaryBitmap(new HybridBinarizer(luminanceSource));

try {
    const decoded = reader.decode(binaryBitmap,hints);

    console.log(decoded)        
} catch (error) {
   // console.log('err',error)
}






console.log(hints)