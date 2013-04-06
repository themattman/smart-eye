var mongo = require('./database.js')
  , email = require('./email.js')
  , stream = require('stream')
  , fs = require('fs')
  , rstream = fs.createReadStream(__dirname + '/../public/test.txt')
  , buf = new Buffer(64)
;

/*mongo.connect(function(msg) {
  if(msg == null)
    console.log("Mongo Connected!");
  else 
    console.log(msg);
});*/

// admin page
exports.admin = function(req, res){
  res.send("<h3> You must be and admin! </h3>");
};

// db test
exports.db = function(req, res){
  mongo.db.collection("test", function(err, collection){
    collection.insert({ msg: "hello world" }, function(err, docs){
      if(err) throw err
      res.send(docs);
    });
  })
};

// main page
exports.index = function(req, res){
  res.render('index', { title: 'Matt Kneiser' });
};

exports.view = function(req, res){
  console.log(req.headers);
  res.render('view', { 'title': 'Matt Kneiser' });
};

exports.stream = function(req, res){
  if(req.method === "GET"){
    /*if(buf.length > 0){
      console.log('success');
      //res.pipe(buf);
    } else {
      console.log('failzorz');
    }*/
    rstream.pipe(res);
    rstream.on('end', function(){
      res.end();
      console.log('dun');
    })
  } else if(req.method === "POST") {
    /*console.log('stream');
    console.log(req.body);
    res.send(req.body);
    req.pipe(buf);*/
    //stream.on('data')
  }
};











