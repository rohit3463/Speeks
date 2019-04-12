const util = require('util');
const path = require('path');
const exec = util.promisify(require('child_process').exec);

async function webm2mp4(inputPath) {
    const inputFile = path.resolve('./') + '/' + inputPath;
    const outputFile = getOutputFileName(inputPath);

    console.log(inputFile, outputFile);

    await exec(`ffmpeg -i ${inputFile} ${outputFile}`);

    return outputFile;
} 

function getOutputFileName(inputPath) {
    const wavFileName = inputPath.slice('uploads/'.length, inputPath.length);
    return path.resolve(`./mp4files/${wavFileName}.mp4`);
}

module.exports = webm2mp4;
