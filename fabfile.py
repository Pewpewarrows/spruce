from fabric.api import run, sudo, put, lcd, local, cd, hosts, execute

def prepare_ppa():
	"""
	Gets the saltstack/salt PPA ready for use
	"""
	sudo('apt-get install -y python-software-properties')
	sudo("add-apt-repository ppa:saltstack/salt -y")
	sudo("apt-get update -y")
	sudo('adduser --no-create-home --disabled-login --system salt')

def bootstrap():
	"""
	Bootstrap a host with a salt minion
	"""
	execute(prepare_ppa)
	# Install the minion
	sudo("apt-get install salt-minion -y")
	sudo('service salt-minion stop')

	put('configs/salt-minion.conf', '/etc/salt/minion', use_sudo=True)
	sudo('service salt-minion start')

def bootstrap_master():
	"""
	Install the salt master
	"""
	execute(prepare_ppa)
	sudo('apt-get install salt-master -y')
	sudo('service salt-master stop')
	
	put('configs/salt-master.conf', '/etc/salt/master', use_sudo=True)
	sudo('service salt-master start')