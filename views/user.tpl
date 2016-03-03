% rebase('base.tpl')
% import interface

<div class="container-fluid">

    <div class="row">

        <div class="col-md-4">
           <div class="userpanel panel panel-default">
               <div class="panel-heading">
                    <h2>{{title}}</h2>
               </div>
               <div class="panel-body">
                   <img src="{{userinfo[1]}}" alt="avatar">
                     % if user is not None and defined('who'):
                     <form id="followform" class="" method="post" action="/follow">
                        <div class="btn-group-vertical" role="group">
                           <input type="submit" class="btn btn-default" name="submit" value="Follow {{who}}">
                           <button class='btn btn-default'><a href="/users/{{who}}">User Page for {{who}}</a></button>
                           <button class='btn btn-default'><a href="/mentions/{{who}}">Mentions of {{who}}</a></button>
                           <input type="hidden" name="who" value="{{who}}">
                        </div>
                     </form>
                     % end

               </div>
           </div>
        </div>


        <div class="col-md-8">

        % for post in posts:
           <div class="panel panel-default">
               <div class="panel-body">
                   <div class="avatar"><img src="{{post[3]}}" alt="avatar"></div>
                   <a class="user" href="/users/{{post[2]}}">@{{post[2]}}:</a>
                   <span class="timestamp">{{post[1]}}</span> <span class="content">{{!interface.post_to_html(post[4])}}</span>
               </div>
           </div>
            % end
        </div>
    </div>  <!-- row -->
</div> <!-- container-fluid -->