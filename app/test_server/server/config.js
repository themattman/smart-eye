var express = require('express')
//  , secret  = require('./secret.js')
  , path    = require('path')
  , passport = require('passport')
;


var allowedDomains = ['smarteye.kunyuchen.com']

var allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', allowedDomains);
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');

    next();
}


module.exports = function configure(app) {
  app.configure(function(){
    app.set('port', process.env.PORT || 3000);
    app.set('views', __dirname + '/../views');
    app.set('view engine', 'jade');
    app.use(express.logger('dev'));
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(app.router);
    app.use(require('less-middleware')({ src: __dirname + '/../public' }));
    app.use(express.static(path.join(__dirname, '/../public')));
    app.use(passport.initialize());
    app.use(allowCrossDomain);
    
    // required password for admins
    /*app.use('/admin', express.basicAuth(function(user, pass){
      return 'user' == user & 'pass' == pass;
    }));*/
  });

  app.configure('development', function(){
    app.use(express.errorHandler());
  });
}