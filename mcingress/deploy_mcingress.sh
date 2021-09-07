kubectl config use-context xonotic-game

kubectl apply -f namespace.yaml

kubectl config use-context xonotic-game-us

kubectl apply -f namespace.yaml

kubectl config use-context xonotic-game

kubectl apply -f deploy.yaml

kubectl config use-context xonotic-game-us

kubectl apply -f deploy.yaml

kubectl get deployment --namespace xonotic-ui

kubectl config use-context xonotic-game

kubectl apply -f mcs.yaml

kubectl get mcs -n xonotic-ui

kubectl apply -f mci.yaml

kubectl describe mci region-ingress -n xonotic-ui
