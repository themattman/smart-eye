var sys     = require('sys')
  , exec    = require('child_process').exec
  , child
  , streams = []
;

function puts(err, stdout, stderr){
  sys.puts(err);
  sys.puts(stdout);
  sys.puts(stderr);
}

// main page
exports.index = function(req, res){
  console.log('GET /');
  res.render('index', { title: 'Matt Kneiser' });
};

exports.stream = function(req, res){
  child = exec("/opt/local/bin/python2.7 ~/Development/face/magnum/recog.py", puts);
  streams[req.params.stream_name] = child.pid;
  console.log(streams)

  res.render('index', { 'title': child.pid });
};