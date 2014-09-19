module.exports = {
    startServer: function() {
	var express = require('express'),
	app = express(),
	bodyParser = require('body-parser'),
	compress = require('compression'),
	errorHandler = require('errorhandler'),
	morgan  = require('morgan'), // logger
	methodOverride = require('method-override');

	app.use(errorHandler({
	    dumpExceptions: true,
	    showStack: true
	}));

	app.use(morgan({
	    format: ':method :url'
	}));

	app.use(bodyParser());

	// Gzip content
	app.use(compress());

	app.use(express.static(__dirname + "/public"));

	app.use(methodOverride());

	app.get('/', function(request, response) {
	    return response.sendfile('public/index.html');
	});

	return app.listen(process.env.PORT || 3333, function() {
	    return console.log("Listening on port 3333…");
	});
    }
};
