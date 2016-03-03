<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>{{title}}</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/style.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">psst</a>
        </div>
        <div class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
              <li><a href="/">Home</a></li>
%if defined('user') and user is not None:
              <li><a href="/my">My Images</a></li>
% end
              <li><a href="/users">Users</a></li>
              <li><a href="/about">About</a></li>
              <li><a href="/static/assignment.html">Assignment Spec</a></li>
            </ul>

%if defined('user') and user is not None:
            <form id='logoutform' class="navbar-form navbar-right pull-right" role="logout" method='post' action='/logout'>
                <input type="submit" class="btn btn-default" name='logout' value='Logout' >
            </form>

            <div class="navbar-text navbar-right pull-right">Logged in as {{user}}</div>

% else:
            <form id='loginform' class="navbar-form navbar-right" role="login" method='post' action='/login'>
		        <div class="form-group">
		          <input type="text" name='nick' class="form-control" placeholder="Username">
		        </div>
		        <div class="form-group">
		          <input type="password" name='password' class="form-control" placeholder="Password">
		        </div>
		        <input type="submit" class="btn btn-default" value='Login' >
		    </form>
% end
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">

        <div class="header">
            <h1></h1>
        </div>
		    {{!base}}

    </div>


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
