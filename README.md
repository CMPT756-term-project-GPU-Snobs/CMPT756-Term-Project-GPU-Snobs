# CMPT756-Term-Project-GPU-Snobs


// Project Commands

// Start service
make -f eks.mak start // start eks cluster

//Set Kubectl context
make -f k8s.mak provision
kubectl config set-context --current --namespace=c756ns

// Provision services & stuff
make -f k8s.mak provision

//Print grafana URL
make -f k8s.mak grafana-url

// Create gatling-1-music.sh
vim -> 
#!/usr/bin/env bash
docker container run --detach --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=`tools/getip.sh kubectl istio-system svc/istio-ingressgateway` \
  -e USERS=1 \
  -e SIM_NAME=ReadMusicSim \
  --label gatling \
  ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
  -s proj756.ReadMusicSim

chmod u+x gatling-1-music.sh
