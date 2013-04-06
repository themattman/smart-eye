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
  var name = req.params.name || req.params.stream_name
  if(name){
    var cmd = "/opt/local/bin/python2.7 ~/Development/face/magnum/recog.py";
    //cmd += (" " + name) || ""; //Different for name
    console.log('[', cmd, ']')
    child = exec(cmd , puts);
    streams[name] = child.pid;
    console.log(streams)
  }else{
    console.log('Bad request: no stream name given')
  }

  res.render('index', { 'title': (child.pid || 'bad') });
};

exports.register = function(req, res){
  console.log('register', req.params.name)
  res.render('index', { 'title': req.params.name });
};