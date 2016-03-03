% rebase('base.tpl')
% import interface

<div class="container-fluid">

    <div class="row">

        <div class="col-md-4">
           <div class="panel panel-default">
               <div class="panel-heading">
                   % if user is not None:
                    <h2>Welcome to FlowTow {{user}}</h2>
                   % else:
                     <h2>Welcome to FlowTow</h2>
                   % end
               </div>
           </div>
        </div>


        <div class="col-md-8">

        %if user is not None:
            <form id='uploadform' class="" method='post' action='/upload' enctype="multipart/form-data">
                <div class="form-group">
                    <input type='file' name='imagefile'>
                    <p class="help-block">Select an image file to upload (JPG, PNG or GIF).</p>
                    <input type="submit" class="btn btn-default" name='submit' value='Submit' >
                </div>
            </form>
        % end

        % for image in images:
        <div class='flowtow'>
            <p><span class='date'>{{image['timestamp']}}</span> <span class='user'>{{image['user']}}</span></p>
            <img src='/static/images/{{image['filename']}}'>
            <p class='likes'>{{image['likes']}} Likes</p>
            <form role='form' method='post' action='/like'>
              <input type='hidden' name='filename' value="{{image['filename']}}">
              <input class='btn btn-primary' type='submit' value='Like'>
            </form>
        </div>
            % end
        </div>
    </div>  <!-- row -->
</div> <!-- container-fluid -->
