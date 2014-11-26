# Note: We're using plurals to denote permissions an ALL applicable objects, and
# singular for permissions on a GIVEN object (which should be specified in the
# 'context' of the auth token data)

# God-mode (i.e. full access).
GOD = 'god'

# Read access to data in network, e.g. apps, player, subnetworks.
# Context required:
#   network
NETWORK__READ = 'network:read'

# Full control for actions of a user within a given (top-level) network,
# e.g. CRUD user-accounts and associated sub-networks for the given network.
# Context required:
#   network
#   user
NETWORK__USER__FULL = 'network.user:full'

# Authenticate / create a user via identities and retrieve new access tokens for
# them, with scopes depending on current context and scopes.
USERS__LOGIN = 'users:login'
USERS__CREATE = 'users:create'

# Wrie access to a users data.
# Context required:
#   user
USER__UPDATE = 'user:update'
