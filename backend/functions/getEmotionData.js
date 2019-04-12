var FormData = require('form-data');
var fs = require('fs');
var fetch = require('node-fetch');

var webm2mp4 = require('./webm2mp4');

async function getEmotionData(videoFilePath) {
    return new Promise(async (resolve, reject) => {
        let form = new FormData();

        let outputFile = await webm2mp4(videoFilePath);
        let readStream = fs.createReadStream(outputFile);
        console.log(outputFile);

        form.append('videoFile', readStream);

        let fetchData = await fetch(process.env.EMOTION_ENDPOINT, {
            method: 'POST',
            mode: 'cors',
            headers: form.getHeaders(),
            body: form,
        });

        let emotionData = await fetchData.text();
        //console.log(confidenceData);
        resolve(emotionData);
    });
}

module.exports = getEmotionData;

