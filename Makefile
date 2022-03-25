SHELL := /bin/bash
all: cli_shortcuts cluster_permissions start_service set_kubectl_context prevision_services print_grafana_url create_gatling_music change_gatling_music_permissions

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