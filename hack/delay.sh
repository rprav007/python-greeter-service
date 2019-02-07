#!/bin/bash
service=$1

pod=`oc get pod -l app=$service -o=jsonpath='{.items[0].metadata.name}'`
oc exec $pod curl http://localhost:8080/setDelay?delay=2
oc label --overwrite pods $pod delay=true
echo "$pod is now slow"

