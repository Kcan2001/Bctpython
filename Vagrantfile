# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.post_up_message = "Hi, you can run 'vagrant ssh' and then 'rs.sh' to run server in vagrant or you can manually run server in your IDE."

  config.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 2
      v.name = "blackcrowtours"
  end

  config.vm.network :forwarded_port, guest: 8000, host: 8000
  config.vm.provision :shell, :path => "vagrant/provision/provision.sh"
  config.vm.provision "shell", :path => "vagrant/provision/provision_always.sh", run: "always"
end
