from fabric.api import run, sudo, put, lcd, local, cd, hosts, execute


def prepare_salt_ppa():
    """
    Gets the saltstack/salt PPA ready for use
    """
    sudo('apt-get install -y python-software-properties')
    sudo('add-apt-repository ppa:saltstack/salt-daily -y')
    sudo('apt-get update -y')
    # sudo('adduser --no-create-home --disabled-login --system salt')


def bootstrap_salt_master():
    """
    Install the salt master
    """
    execute(prepare_salt_ppa)

    sudo('apt-get install salt-master -y --force-yes')
    sudo('service salt-master stop')

    put('conf/salt/master.conf', '/etc/salt/master', use_sudo=True)
    sudo('mkdir -p /srv/salt/states')
    sudo('service salt-master start')


def bootstrap_salt_minion():
    """
    Bootstrap a host with a salt minion
    """
    execute(prepare_salt_ppa)
    # Install the minion
    sudo('apt-get install salt-minion -y --force-yes')
    sudo('service salt-minion stop')

    put('conf/salt/minion.conf', '/etc/salt/minion', use_sudo=True)
    sudo('service salt-minion start')
