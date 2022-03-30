#!/bin/sh

# start services
make -f eks.mak start

# start previsions
make -f k8s.mak provision

# prevision context
kubectl config set-context --current --namespace=c756ns

# print grafana url
make -f k8s.mak grafana-url

#print kiali url
make -f k8s.mak kiali-url