#!/bin/bash
service=$1

pod=`oc get pod -l app=$service -o=jsonpath='{.items[0].metadata.name}'`
oc exec $pod curl http://localhost:8080/misbehave
oc label --overwrite pods $pod misbehave=true
echo "$pod is now misbehaving"

