# CMPT756-Term-Project-GPU-Snobs

## Service Running instructions
Follow the instructions below to get the project running on your local machine. Please note that these instructions were tested on linux x86 machine and Macos x86. <br> <br>

#### 1. Make sure that your are in the CMPT756-Term-Project-GPU-Snobs directory. <br> <br>
#### 2. Add following information to **.ec2.mak file** in the cli_shortcuts directory
- your AWS security group ID
- Name of the EC2 key
- Path to the .pem file including the name


#### 3. Make sure to create a personal access token (PAT) for your GitHub account. You will need the three scopes: read:packages, write:packages and delete:packages. Save the token in the cluster/ghcr.io-token.txt file <br> <br>

#### 4. Run **./tools/shell.sh** file

#### 5. run **make all** command to start the service
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
