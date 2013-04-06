var express = require('express')
  , app     = express()
  , colors  = require('colors')
  , router  = require('./router.js')
  , config  = require('./config.js')
  , http    = require('http')
  , sys     = require('sys')
  , exec    = require('child_process').exec
  , child
;

//setInterval(function(){child = exec("ps", puts);}, 5000);

// setup here
config(app);


// ---------------------------------------------------------- //
// define API routes here
// ---------------------------------------------------------- //
// GET
app.get('/',                    router.index);
app.get('/stream/:stream_name', router.stream)
// ---------------------------------------------------------- //
// ---------------------------------------------------------- //


// start the server
var httpApp = http.createServer(app).listen(app.get('port'), function(){
  console.log(("Express server listening on port " + app.get('port')).blue);
  setInterval(function(){
    console.log('Intervalling...', new Date());

    // Send REQ's to the other server
  }, 5000);
});