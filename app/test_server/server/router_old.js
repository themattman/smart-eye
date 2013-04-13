/*var sys     = require('sys')
  , exec    = require('child_process').exec
  , child
  , streams = []
;

// main page
exports.index = function(req, res){
  console.log('GET /');
  res.render('index', { title: 'Matt Kneiser' });
};

exports.stream = function(req, res){
  //if(req.method == 'POST'){
  if(req.method == 'GET'){
    console.log(req.body);
    console.log('ip =', req.body['ip']);
    console.log('port =', req.body['port']);
    var name = req.params.name || req.params.stream_name;
    if(name){
      console.log('stream');
      console.log(streams[name]);

      // Only set up a connection if it 
      if(!streams[name]){
        console.log('not streams[name]');
        streams[name] = req.body;
        var cmd = "/opt/local/bin/python2.7 ~/Development/face/magnum/recog.py";
        //cmd += " rtsp://" + req.body['ip'] + ':' + req.body['port'];
        console.log('[', cmd, ']');
        child = exec(cmd , function(err, stdout, stderr){
          console.log('name', name);
          delete streams[name];
        });
        streams[name].pid = child.pid;
      }
    }else{
      console.log('Bad request: no stream name given')
    }
  }else{
    console.log('GET /STREAM/:ID')
    //res.render('index', { 'title': (child.pid || 'bad') });
    res.render('index', { 'title': 'bad' });
  }
};

exports.register = function(req, res){
  console.log('register', req.params.name)
  res.render('index', { 'title': req.params.name });
};

exports.trigger = function(req, res){
  console.log('TRIGGER FOUND -', req.params.id);
};*/

// Mux the stream for live viewing online
// email the img to the user's email
// account system? (config file, ppl auth at the web server and the camera is trusting)
// assume ppl use this on the local network

/**
 * Variables for Socket.IO and HTTP server
 **/
var express        = require('express')
  , app            = express()
  , config         = require('./config.js')
  , http           = require('http')
  , basedir        = __dirname// + '/../'
  , imgdir         = '/img/' // Where JPGs are going to be stored
  , io             = require('socket.io').listen(8081)
  , fs             = require('fs')
  , path           = require('path')
  , STREAM         = '/img_now2.avi'
;

config(app)

/**
 * Request manager from Express, using authentication with passport-http to send
 * client/index.html
 **/
app.get('/', function (req, res) {
  res.sendfile(path.normalize(basedir) + 'client/index.html');
});
app.get('/iribarren.jpg', function (req, res) {
  res.sendfile(path.normalize(basedir) + 'client/iribarren.jpg');
});
app.get('/stream2', function(req, res) {
  res.sendfile(path.normalize(basedir) + STREAM);
});
app.get('/stream', function(req, res) {
  console.log(path.normalize(basedir) + '/img.mpg');
  res.sendfile(path.normalize(basedir) + '/img.mpg');//'img/001_camaraip.jpg');
});
app.get('/002.jpg', function(req, res) {
  res.sendfile(path.normalize(basedir) + 'img/002_camaraip.jpg');
});

// start the server
var httpApp = http.createServer(app).listen(app.get('port'), function(){
  console.log(("Express server listening on port " + app.get('port')));
});

/**
 * Users for the system
 **/
var users = [
    { username: 'alcaldia', password: 'amalia saez'}
  , { username: 'desur', password: 'cedeno'}
  , { username: 'jorge', password: 'una contrasena muy fuerte'}
  , { username: 'sts', password: 'sin contrasena'}
  , { username: 'amtt', password: 'amtt'}
];

function findByUsername(username, fn) {
  for (var i = 0, len = users.length; i < len; i++) {
    var user = users[i];
    if (user.username === username) {
      console.log('USERNAME CORRECT')
      return fn(null, user);
    }
  }
  return fn(null, null);
}

/**
 * Configuring Socket.IO
 **/
io.configure('prod', function(){
  io.enable('browser client minification');
  io.enable('browser client etag');
  io.enable('browser client gzip');
  io.set('log level', 1);

  io.set('transports', [
    'websocket'
  , 'flashsocket'
  , 'htmlfile'
  , 'xhr-polling'
  , 'jsonp-polling'
  ]);
});

io.configure('dev', function(){
  io.set('transports', ['websocket']);
});

/**
 * Declaring inputs and outputs for the cameras
 **/
var inputs = [
  //"rtsp://67.194.194.201:8086"
  //"rtsp://172.16.0.66:8086"
  "rtsp://67.194.178.242:8086"
  //"/Users/mattman/Downloads/IMG_0288.MOV"
  //, "rtsp://admin:admin@192.168.71.23/0"
  ],
  outputs = [
  "001"
  ],
  totalchildren = inputs.length,
  children = new Array(totalchildren),
  loop = undefined,
  frequency=10;

var checker = function() {
  loop = setInterval( function() {
    for (var i = 0; i < totalchildren; i++) {
      if (children[i] == undefined) {
        callFFmpeg( i, inputs[i], outputs[i]);
      }
    };
  }, frequency*1000);
}

var rate = 4,
    suffixout = 'camaraip',
    outextension = 'jpg';

function callFFmpeg (i, input, prefixout) {

  /**
   * Variables for FFmpeg
   **/
  var util = require('util')
    , exec = require('child_process').exec
    , rate = 4 // Video FPS rate.
    , quality = 'qvga' // Quality of the image
    , extraparams = '-b:v 32k'
    , suffixout = 'camaraip' // Suffix for the JPEG output of FFmpeg
      //    prefixout001 = '001', prefixout002 = '002'
    , outextension = 'jpg'
  ;

  /**
   * Call to FFmpeg
   **/
  console.log('ffmpeg -i ' + input + ' ./server' + STREAM)// + ' -r ' + rate + ' -s ' + quality + ' ' + extraparams + ' -f image2 -updatefirst 1 ' + basedir + imgdir + prefixout + '_' + suffixout + '.' + outextension);
  children[i] = exec('ffmpeg -i ' + input + ' ./server' + STREAM// + ' -r ' + rate + ' -s ' + quality + ' ' + extraparams + ' -f image2 -updatefirst 1 ' + basedir + imgdir + prefixout + '_' + suffixout + '.' + outextension
    , {maxBuffer: 2048*1024},
    function (error, stdout, stderr) {
      if (error !== null) {
        console.error('FFmpeg\'s ' + prefixout + ' exec error: ' + error);
      }
  });

  children[i].on('exit', function (code) {
    console.log('FFmpeg child: ' + inputs[i] + ' exited and is being re-launched');
    children[i] = undefined;
  });
  children[i].on('SIGTERM', function() {
    console.log('FFmpeg child: ' + inputs[i] + ' got terminated and is being re-launched');
    children[i] = undefined;
  });
}


/**
 * Calling checker()
 **/
checker();

/**
 * Calling function `callSocket` to get Socket.IO running
 **/
callSocket('001');
//callSocket('002');

function callSocket (cam) {
  console.log('cam')
  console.log(cam)
  io.of('/' + cam).on('connection', function (client) {
    console.log('client')
    console.log(client)
    /**
     * @name imageWatcher
     * @desc Watchdog for any change on image files
     * @params complete file path
     **/
  //  var imgcount = 0;
    console.log( basedir + imgdir);
    setInterval( function() {
      fs.readFile( basedir + imgdir + cam + '_' + suffixout + '.' + outextension,
        function(err, content) {
          if (err) {
            throw err;
          } else {
  //          ++imgcount;
  //          console.log( 'Transformation #' + imgcount);
            client.volatile.emit('message', {
              data: content.toString('base64')
            });
          }
        });
    }, 1000/rate);
  });
}
