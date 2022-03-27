SHELL := /bin/bash
all: start_service prevision_services prevision_context print_grafana_url

cli_shortcut:
	cp cli_shortcuts/.aws-a ~/
	cp cli_shortcuts/.aws-off ~/
	cp cli_shortcuts/.ec2.mak ~/
	source ~/.aws-a
	
cluster_permissions:
	chmod go-rwx cluster
	chmod go-rwx cluster/*
	chmod a+rwx eks.mak
	chmod a+rwx k8s.mak

start_service:
	make -f eks.mak start

set_kubectl_context:
	make -f k8s.mak provision kubectl config set-context --current --namespace=c756ns

prevision_services:
	make -f k8s.mak provision

prevision_context:
	kubectl config set-context --current --namespace=c756ns

print_grafana_url:
	make -f k8s.mak grafana-url

create_gatling_music:
	vim -> #!/usr/bin/env bash docker container run --detach --rm
	-v ${PWD}/gatling/results:/opt/gatling/results
	-v ${PWD}/gatling:/opt/gatling/user-files
	-v ${PWD}/gatling/target:/opt/gatling/target
	-e CLUSTER_IP=tools/getip.sh kubectl istio-system svc/istio-ingressgateway
	-e USERS=1
	-e SIM_NAME=ReadMusicSim
	--label gatling
	ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2
	-s proj756.ReadMusicSim

change_gatling_music_permissions:
	chmod u+x gatling-1-music.sh

test_print:
	echo "Test is working"

install_kubctl:
	curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
	sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
	kubectl version --client
	
install_eks_ctl:
	curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
move_eks_ctl:
	sudo mv /tmp/eksctl /usr/local/bin
check_eks_ctl_version:
	eksctl version
download_istio:
	curl -L https://istio.io/downloadIstio | sh -
	
istio_path:
	export PATH=$(PWD)/istio-1.13.2/bin:$(PATH)
install_istio:
	istioctl install --set profile=demo -y
	kubectl label namespace default istio-injection=enabled

install_dependencies:
	sh install_dependencies.sh