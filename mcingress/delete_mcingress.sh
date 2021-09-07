# kubectl describe mci region-ingress -n xonotic-ui

kubectl get mcs -n xonotic-ui

kubectl delete -f mci.yaml

kubectl config use-context xonotic-game

kubectl delete -f mcs.yaml

kubectl config use-context xonotic-game-us

kubectl delete -f deploy.yaml

kubectl get deployment --namespace xonotic-ui

kubectl config use-context xonotic-game

kubectl delete -f deploy.yaml

kubectl config use-context xonotic-game-us

kubectl delete -f namespace.yaml

kubectl config use-context xonotic-game

kubectl delete -f namespace.yaml

#

gcloud alpha container hub ingress disable
