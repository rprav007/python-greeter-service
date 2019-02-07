#!/bin/bash
service=$1

pod=`oc get pod -l app=$service,misbehave=true -o=jsonpath='{.items[0].metadata.name}'`
echo ""
oc exec $pod curl http://localhost:8080/behave
oc label --overwrite pods $pod misbehave=false
echo "$pod is now behaving"
