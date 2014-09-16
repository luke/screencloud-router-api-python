from werkzeug.local import Local, LocalManager

# Our global (per request) object.  Framework agnostic to make it easier to
# switch things.
g = Local()
local_manager = LocalManager([g])
