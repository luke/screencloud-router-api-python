# Note: We're using plurals to denote permissions an ALL applicable objects,
# singular for permissions on a GIVEN object (id should be provided in the data)

# God-mode (i.e. full access).
GOD = 'god'

# Read access to data in network, e.g. apps, player, subnetworks.
#   network_id
NETWORK__READ = 'network:read'

# Create new sub-networks in network.
#   network_id
NETWORK__SUB_NETWORKS = 'network:sub-networks:full'

# Full control for actions of a user within a given network, e.g. CRUD user
# accounts within a sub-network for the given network.
#   network_id
#   user_id
NETWORK__USER__FULL = 'network:user:full'


USERS__LOGIN = 'users:login'
USERS__CREATE = 'users:create'
