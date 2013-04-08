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
  if(req.method == 'POST'){
    console.log(req.body);
    console.log('ip =', req.body['ip']);
    console.log('port =', req.body['port']);
    //console.log(req.connection.remoteAddress)
    var name = req.params.name || req.params.stream_name
    if(name){
      console.log('stream');
      console.log(streams[name]);
      if(!streams[name]){
        console.log('not streams[name]')
        streams[name] = req.body;
        var cmd = "/opt/local/bin/python2.7 ~/Development/face/magnum/recog.py";
        cmd += " rtsp://" + req.body['ip'] + ':' + req.body['port'];
        console.log('[', cmd, ']')
        child = exec(cmd , puts);
        streams[name].pid = child.pid;
        console.log(streams)
      }
    }else{
      console.log('Bad request: no stream name given')
    }
  }else{
    console.log('GET /STREAM/:ID')
    res.render('index', { 'title': (child.pid || 'bad') });
  }
};

exports.register = function(req, res){
  console.log('register', req.params.name)
  res.render('index', { 'title': req.params.name });
};

exports.trigger = function(req, res){
  console.log('TRIGGER FOUND -', req.params.id);
};