const sdk = require('microsoft-cognitiveservices-speech-sdk');
const fs = require('fs');


function speech2text(fileName) {
    return new Promise((resolve, reject) => {
        sdk.Recognizer.enableTelemetry(false);
        let pushStream = sdk.AudioInputStream.createPushStream();

        const subsciptionKey = process.env.subsciptionKey;
        const serviceRegion = process.env.serviceRegion;

        fs.createReadStream(fileName)
        .on('data', (arrayBuffer) => {
            pushStream.write(arrayBuffer.buffer);
        })
        .on('end', () => {
            pushStream.close();
        });

        console.log('Starting Speech Recognition');

        let audioConfig = sdk.AudioConfig.fromStreamInput(pushStream);
        let speechConfig = sdk.SpeechConfig.fromSubscription(subsciptionKey, serviceRegion);
        speechConfig.speechRecognitionLanguage = 'en-US';

        let recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

        recognizer.recognizeOnceAsync((result) => {
            console.log(result);
            recognizer.close();
            recognizer = undefined;

            resolve(result);
        }, (err) => {
            console.log('Error in Speech2Text');
            console.log(err);

            recognizer.close();
            recognizer = undefined;

            reject(undefined);
        });
    });

}

module.exports = speech2text;
