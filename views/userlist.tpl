% rebase('base.tpl')
% import interface

<div class="container-fluid">


    % for r in range(int(len(users)/4)):
    <div class="row">

        % for c in range(4):
          % u = users[r*4+c]
        <div class="col-xs-6 col-md-3">
            <div class="thumbnail">
                   <img src="{{u[1]}}" alt="avatar">
                   <div class='caption'>
                   <h3><a class="user" href="/users/{{u[0]}}">@{{u[0]}}</a></h3>
                   </div>
             </div>
        </div>
        % end

    </div>  <!-- row -->
    % end
</div> <!-- container-fluid -->