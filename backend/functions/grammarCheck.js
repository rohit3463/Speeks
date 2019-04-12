const speech2text = require('./speech2text');
const ptClient = require('perfecttense');

async function checkGrammar(wavFilePath) {
    ptClient.initialize({
        appKey: process.env.GRAMMAR_APP_KEY
    });

    let result = await speech2text(wavFilePath);
    let text = result.privText;

    ptClient.submitJob(text, process.env.GRAMMAR_API_KEY, undefined, ['grammarScore', 'offset'])
    .then(success, faliure);
}

function success(result) {
    console.log(JSON.stringify(result));

    let response = {
        grammarScore: 0.0,
        table: null,
    }, 
    tableData = {
        grammar: [],
        verb: [],
        determiner: [],
        pronoun: [],
    }, 
    correctionData = {
        affected: '',
        corrected: '',
        message: '',
    };

    const corrections = result.offset[0].corrections;
    console.log(corrections);

    for(let i = 0 ; i < corrections.length ; ++i) {
        const ruleID = corrections[i].options[0].appliedRules[0].ruleId.charAt(0);

        if(ruleID === '0') {
            correctionData.affected = corrections[i].options[0].affected;
            correctionData.corrected = corrections[i].options[0].corrected;
            correctionData.message = corrections[i].options[0].appliedRules[0].message;
            tableData.grammar.push(correctionData);
        }

        else if(ruleID === '2') {
            correctionData.affected = corrections[i].options[0].affected;
            correctionData.corrected = corrections[i].options[0].corrected;
            correctionData.message = corrections[i].options[0].appliedRules[0].message;
            tableData.verb.push(correctionData);
        }
            
        else if(ruleID === '3') {
            correctionData.affected = corrections[i].affected;
            correctionData.corrected = corrections[i].options[0].corrected;
            correctionData.message = corrections[i].options[0].appliedRules[0].message;
            tableData.determiner.push(correctionData);
        }
            
        else if(ruleID === '5') {
            correctionData.affected = corrections[i].options[0].affected;
            correctionData.corrected = corrections[i].options[0].corrected;
            correctionData.message = corrections[i].options[0].appliedRules[0].message;
            tableData.pronoun.push(correctionData);
        }
    }

    response.grammarScore = result.grammarScore;
    response.table = tableData;

    console.log(JSON.stringify(response));
}

function faliure(err) {
    console.log('Grammar: Perfect Tense API Error');
    console.log(err);
}

module.exports = checkGrammar;