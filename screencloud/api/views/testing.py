from flask import Blueprint, render_template_string, url_for

from screencloud import config
from .. import g

bp = Blueprint(__name__, __name__)

@bp.route('/google', methods=['GET'])
def google():
    template = '''
<html>
  <head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
  </head>
  <body>
    <!-- Add where you want your sign-in button to render -->
    <div id="signinButton">
      <span class="g-signin"
        data-scope="https://www.googleapis.com/auth/plus.login"
        data-clientid="{{ client_id }}"
        data-redirecturi="postmessage"
        data-accesstype="offline"
        data-cookiepolicy="single_host_origin"
        data-callback="signInCallback"
        {% if force_prompt %}data-approvalprompt="force"{% endif %}
      >
      </span>
    </div>
    <div id="result"></div>

    <script type="text/javascript">
    function signInCallback(authResult) {
      if (authResult['code']) {

        // Hide the sign-in button now that the user is authorized, for example:
        //$('#signinButton').attr('style', 'display: none');

        // Send the code to the server
        $.ajax({
          type: 'POST',
          url: '{{ callback_url }}',
          success: function(result) {
            // Handle or verify the server response if necessary.

            // Prints the list of people that the user has allowed the app to know
            // to the console.
            console.log(result);
            if (result['profile'] && result['people']){
              $('#results').html('Hello ' + result['profile']['displayName'] + '. You successfully made a server side call to people.get and people.list');
            } else {
              $('#results').html('Failed to make a server-side call. Check your configuration and console.');
            }
          },
          data: {
            code: authResult['code']
          }
        });
      } else if (authResult['error']) {
        // There was an error.
        // Possible error codes:
        //   "access_denied" - User denied access to your app
        //   "immediate_failed" - Could not automatially log in the user
        // console.log('There was an error: ' + authResult['error']);
      }
    }
    </script>


    <script type="text/javascript">
      (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();
    </script>
  </body>
</html>
'''
    return render_template_string(
        template,
        client_id=config['OAUTH_CLIENTS']['google']['client_id'],
        callback_url=url_for('.google_callback'),
        force_prompt=True,
    )

@bp.route('/google/callback', methods=['POST'])
def google_callback():
    code = g.request.form.get('code')

    from oauth2client.client import OAuth2WebServerFlow
    flow = OAuth2WebServerFlow(
        client_id=config['OAUTH_CLIENTS']['google']['client_id'],
        client_secret=config['OAUTH_CLIENTS']['google']['client_secret'],
        scope='',
        redirect_uri='postmessage'
    )
    credentials = flow.step2_exchange(code)

    import json
    return json.dumps(credentials.token_response)
