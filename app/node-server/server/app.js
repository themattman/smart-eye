var express = require('express')
  , app     = express()
  , colors  = require('colors')
  , router  = require('./router.js')
  , config  = require('./config.js')
  , http    = require('http');

// setup here
config(app);


// ---------------------------------------------------------- //
// define API routes here
// ---------------------------------------------------------- //
// GET
app.get('/',      router.index);
app.get('/admin', router.admin);
app.get('/db',    router.db   );
app.get('/view',  router.view );
app.all('/stream', router.stream);
// ---------------------------------------------------------- //
// ---------------------------------------------------------- //


// start the server
var httpApp = http.createServer(app).listen(app.get('port'), function(){
  console.log(("Express server listening on port " + app.get('port')).blue);
});