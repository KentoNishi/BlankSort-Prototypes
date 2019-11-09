var express = require('express'),
    app = express();

// app.use("../tests", express.static("tests"));

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.listen(8000);