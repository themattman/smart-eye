var express = require('express')
//  , secret  = require('./secret.js')
  , path    = require('path');

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
    
    // required password for admins
    app.use('/admin', express.basicAuth(function(user, pass){
      return 'user' == user & 'pass' == pass;
    }));
  });

  app.configure('development', function(){
    app.use(express.errorHandler());
  });
}