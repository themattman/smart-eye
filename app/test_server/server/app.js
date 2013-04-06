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

function puts(err, stdout, stderr){
  sys.puts(err);
  sys.puts(stdout);
  sys.puts(stderr);
}
//child = exec("while [ true ]; do ls -la; done", puts);
//child = exec("ls -la", puts);
//child = exec("pwd", puts);
child = exec("/opt/local/bin/python2.7 ~/Development/face/magnum/recog.py", puts);
console.log(child.pid)
//setInterval(function(){child = exec("ps", puts);}, 5000);

// setup here
config(app);


// ---------------------------------------------------------- //
// define API routes here
// ---------------------------------------------------------- //
// GET
app.get('/', router.index);
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