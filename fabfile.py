import uuid
from fabric.api import run, sudo, put, lcd, local, cd, hosts, execute, get

SALT_MASTER_SERVER = 'salt@192.168.0.85'

SALT_MASTER_USERNAME, SALT_MASTER_IP = SALT_MASTER_SERVER.split('@')

def prepare_salt_ppa():
    """
    Gets the saltstack/salt PPA ready for use
    """
    sudo('apt-get install -y python-software-properties')
    sudo("add-apt-repository ppa:saltstack/salt -y")
    sudo("apt-get update -y")

@hosts(SALT_MASTER_SERVER)
def get_minion_key(minion_id):
    """
    Given a minion ID, generate a keypair for the minion on the
    salt master and pull it down as minion.pub and minion.pem, then
    delete the private key from the master.
    """
    sudo('salt-key --gen-keys=%s' % minion_id)
    sudo('chmod 644 %s.pub %s.pem' % (minion_id, minion_id))
    get('%s.pub' % minion_id, 'minion.pub')
    get('%s.pem' % minion_id, 'minion.pem')
    sudo('cp %s.pub /etc/salt/pki/minions/%s' % (minion_id, minion_id))
    run('rm -f %s.pem' % minion_id)
    run('rm -f %s.pub' % minion_id)
    sudo('chown -R root.root /etc/salt')

def bootstrap_salt_minion():
    """
    Bootstrap a host with a salt minion
    """
    execute(prepare_salt_ppa)
    
    # Let the master generate the key
    minion_id = uuid.uuid4()
    execute(get_minion_key, minion_id)

    # Push the key and configuration to the minion
    sudo('mkdir -p /etc/salt/pki')
    put('conf/salt/minion.conf', '/etc/salt/minion', use_sudo=True)
    put('minion.pem', '/etc/salt/pki/minion.pem', use_sudo=True)
    put('minion.pub', '/etc/salt/pki/minion.pub', use_sudo=True)
    sudo('chown -R root.root /etc/salt')
    local('rm minion.pem minion.pub')

    # Patch the config file to contain the minion ID and proper master address
    sudo("sed -i -e 's/#id:/id: %s/' /etc/salt/minion" % minion_id)
    sudo("sed -i -e 's/#master:/master: %s/' /etc/salt/minion" % SALT_MASTER_IP)

    # Install the minion
    sudo("apt-get install salt-minion -y")

@hosts(SALT_MASTER_SERVER)
def bootstrap_salt_master():
    """
    Install the salt master
    """
    execute(prepare_salt_ppa)
    sudo('apt-get install salt-master -y')
    sudo('service salt-master stop')
    
    put('conf/salt/master.conf', '/etc/salt/master', use_sudo=True)
    sudo('mkdir -p /srv/salt/states')
    sudo('service salt-master start')
