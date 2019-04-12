const getConfidenceData = require('../functions/getConfidenceData');
const getEmotionData = require('../functions/getEmotionData');
const getSpeechEmotion = require('../functions/getSpeechEmotion');

async function apiController(inputFile) {
    let confidenceData = await getConfidenceData(inputFile.path);
    console.log(confidenceData);

    let emotionData = await getEmotionData(inputFile.path);
    console.log(emotionData);

    let speechEmotion = await getSpeechEmotion(inputFile.path);
    console.log(speechEmotion);

    return "Incomplete Data";
} 

module.exports = apiController;