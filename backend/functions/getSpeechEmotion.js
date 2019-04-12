var FormData = require('form-data');
var fs = require('fs');
var fetch = require('node-fetch');
var path = require('path');

async function getConfidenceData(videoFilePath) {
    return new Promise(async (resolve, reject) => {
        let form = new FormData();

        let fileName = getOutputFileName(videoFilePath);
        let readStream = fs.createReadStream(fileName);
        console.log(fileName, process.env.SPEECH_EMOTION_ENDPOINT);

        form.append('wavFile', readStream);

        let fetchData = await fetch(process.env.SPEECH_EMOTION_ENDPOINT, {
            method: 'POST',
            mode: 'cors',
            headers: form.getHeaders(),
            body: form,
        });

        let speechemotiondata = await fetchData.text();
        //console.log(confidenceData);
        resolve(speechemotiondata);
    });
}

function getOutputFileName(inputPath) {
    const wavFileName = inputPath.slice('uploads/'.length, inputPath.length);
    return path.resolve(`./wavfiles/${wavFileName}.wav`);
}

module.exports = getConfidenceData;