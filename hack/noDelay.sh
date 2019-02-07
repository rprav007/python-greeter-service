#!/bin/bash
service=$1

pod=`oc get pod -l app=$service,delay=true -o=jsonpath='{.items[0].metadata.name}'`
echo ""
oc exec $pod curl http://localhost:8080/setDelay?delay=0
oc label --overwrite pods $pod delay=false
echo "$pod is now fast"
