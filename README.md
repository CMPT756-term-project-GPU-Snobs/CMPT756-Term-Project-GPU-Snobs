# CMPT756-Term-Project-GPU-Snobs

# Project Commands

## Preliminary Set up (Before scripts)
1. Start service
  - make -f eks.mak start

2. Provision services and set Kubectl context
  - make -f k8s.mak provision
  - kubectl config set-context --current --namespace=c756ns

2.5. If the playlist DB not in dynamoDB, run the following
  - aws cloudformation delete-stack --stack-name db-<GITHUB_ID>
  - aws cloudformation create-stack --stack-name db-<GITHUB_ID> --template-body file://cluster/cloudformationdynamodb.json

3. Print grafana URL
  - make -f k8s.mak grafana-url

4. Create gatling-1-music.sh
  - vim -> 
    #!/usr/bin/env bash
    docker container run --detach --rm \
      -v ${PWD}/gatling/results:/opt/gatling/results \
      -v ${PWD}/gatling:/opt/gatling/user-files \
      -v ${PWD}/gatling/target:/opt/gatling/target \
      -e CLUSTER_IP=`tools/getip.sh kubectl istio-system svc/istio-ingressgateway` \
      -e USERS=1 \
      -e SIM_NAME=ReadMusicSim \
      -label gatling \
      ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
      -s proj756.ReadMusicSim

5. Make gatling-1-music.sh runnable
  - chmod u+x gatling-1-music.sh


## Push image service s3 to ghcr

- NOTE: Replace REGID with github ID

1. Build the image (RUN THIS IN S3 FOLDER)
  - docker image build --platform linux/amd64 -t cmpt756s3 .

2. Login to ghcr
  - cat ../cluster/ghcr.io-token.txt | docker login ghcr.io -u REGID --password-stdin

3. Tag the image
  - docker image tag cmpt756s3 ghcr.io/REGID/cmpt756s3:v1

4. Push the image
  - docker image push ghcr.io/REGID/cmpt756s3:v1

5. Validate that the image is updated in github

6. Make the image public in github

## Manually Deploy the service to cluster

1. Replace line 59 of s3.yaml with the following (replace REGID here as well)

  - image: 'ghcr.io/REGID/cmpt756s3:v1'

2. 
  - kubectl -n c756ns apply -f cluster/s3.yaml | tee logs/s3.log

3.
  - k9s -n c756ns
