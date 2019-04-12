var s2t = require('../functions/speech2text');
require('dotenv').config();

console.log(typeof(process.env.subsciptionKey), typeof( process.env.serviceRegion));

let result = s2t('/home/spooderman/Documents/upgrad-backend/wavfiles/2dbc975c77b8cf1abfda253ba62da5cb.wav');

result.then((r) => {console.log(r.privText)});
result.catch((err) => {console.log('err')});