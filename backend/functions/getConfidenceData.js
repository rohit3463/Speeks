var FormData = require('form-data');
var fs = require('fs');
var fetch = require('node-fetch');

var webm2wav = require('./webm2wav');

async function getConfidenceData(videoFilePath) {
    return new Promise(async (resolve, reject) => {
        let form = new FormData();

        let outputFile = await webm2wav(videoFilePath);
        let readStream = fs.createReadStream(outputFile);
        console.log(outputFile);

        form.append('wavFile', readStream);

        let fetchData = await fetch(process.env.CONFIDENCE_ENDPOINT, {
            method: 'POST',
            mode: 'cors',
            headers: form.getHeaders(),
            body: form,
        });

        let confidenceData = await fetchData.text();
        //console.log(confidenceData);
        resolve(confidenceData);
    });
}

module.exports = getConfidenceData;