var sys     = require('sys')
  , exec    = require('child_process').exec
  , fs      = require('fs')
  , child
  , streams = []
  //, io      = require('socket.io').listen(9000)
  , clients = []
;

// main page
exports.index = function(req, res){
  console.log('GET /');
  res.render('index', { title: 'Matt Kneiser' });
};

exports.stream = function(req, res){
  //if(req.method == 'POST'){
  if(req.method == 'POST'){
    console.log(req.body)
    console.log(req.body.emails)
    req.body.emails = JSON.parse(req.body.emails)
    console.log(req.body);
    console.log('ip =', req.body['ip']);
    console.log('port =', req.body['port']);
    var email_addresses = req.body['emails'];
    var name = req.params.name || req.params.stream_name;
    if(name && email_addresses.length > 0){
      console.log('stream');
      console.log(streams[name]);

      // Only set up a connection if it 
      if(!streams[name]){
        console.log('not streams[name]');
        streams[name] = req.body;
        //var cmd = "/opt/local/bin/python2.7 ~/Development/face/magnum/recog.py";
        var cmd = "/opt/local/bin/python2.7 ./server/recog.py";
        cmd += " rtsp://" + req.body['ip'] + ':' + req.body['port'];
        //cmd += " rtsp://67.194.205.140:8086"
        //cmd += " rtsp://67.194.178.242:8086"
        for(var i in email_addresses){
          cmd += " " + email_addresses[i]
        }
        console.log('[', cmd, ']');
        child = exec(cmd , function(err, stdout, stderr){
          console.log(stdout)
          console.log(stderr)
          console.log('name', name);
          delete streams[name];
        });
        streams[name].pid = child.pid;
      }
    }else{
      console.log('Bad request: no stream name given')
    }
  }else if(req.method = 'GET'){
    console.log('GET /STREAM/:ID')
    //res.render('index', { 'title': (child.pid || 'bad') });
    console.log(req.params.stream_name)
    res.render('index', { 'title': 'socket.io', 'MJPGsrc': '/feed/'+req.params.stream_name });
  }
};

exports.feed = function(req, res){
  console.log('feed!')
  var fname = './public/feed/' + req.params.fname;
  console.log(fname)

  //var boundary = 'helloworld'
  //res.setHeader('Cache-Control', 'no-cache');

  //res.setHeader('Content-Type', 'multipart/x-mixed-replace;boundary="' + boundary + '"');
  res.setHeader('Connection', 'close');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Cache-Control', 'no-cache, private');
  res.setHeader('Expires', 0);
  res.setHeader('Max-Age', 0);

  rs = fs.createReadStream(fname);
  rs.on('open', function(){
    console.log('file opened')
    rs.pipe(res);
  });
  /*rs.on('end', function(){
    res.end('--'+boundary+'--');
  });*/
  rs.on('error', function(err){
    res.end(err);
  });
  //res.send('bi')
};

/*io.sockets.on('connection', function (socket) {
  console.log('client =', socket.id)
  clients.push(socket.id)
  io.socket
});*/

exports.register = function(req, res){
  console.log('register', req.params.name)
  res.render('index', { 'title': req.params.name });
};

exports.trigger = function(req, res){
  console.log('TRIGGER FOUND -', req.params.id);
};

// Mux the stream for live viewing online
// email the img to the user's email
// account system? (config file, ppl auth at the web server and the camera is trusting)
// assume ppl use this on the local network