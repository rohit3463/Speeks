var router = require('express').Router();
var multer = require('multer');
var cors = require('cors');

var upload = multer({dest: 'uploads/'});

var apiController = require('../controller/api');

router.post('/', cors(), upload.single('audioVideoData'), async (req, res) => {
    console.log(JSON.stringify( req.file));
    
    let resData = await apiController(req.file);
    res.send(resData);
});

module.exports = router;