## ansible part

This will basically setup on the remote host ( here server ) what is necessary
for the docker-compose to run and be launched by ansible

Assumption made here in this case, the vm is running UBUNTU 20.04 and network setup is done

Used useful roles from geerlingguy that take care of docker installation ( compose included )
as well as pip and required modules for ansible docker_compose

main playbook install_compose_up is doing the installation of components + docker compose up
compose_up is doing the strict compose up ( could have factored code in task/role and include it)
compose_down is doing the strict compose down

to run this:\
ansible-galaxy role install -r requirements.yaml
is required

then:\
ansible-playbook install_compose_up.yaml -K --ask-vault-pass

-K as become:true is required\
--ask-vault-pass as env file for docker compose has been encrypted ( it contains sensible information see sample)\

for other playbooks
- ansible-playbook compose_up.yaml -K
- ansible-playbook compose_down.yaml -K
