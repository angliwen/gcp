git clone https://github.com/GoogleCloudPlatform/terraformer.git && cd terraformer/

go mod download

go build -v

go run build/main.go google

terraform init

# 

export PROVIDER=google
curl -LO https://github.com/GoogleCloudPlatform/terraformer/releases/download/$(curl -s https://api.github.com/repos/GoogleCloudPlatform/terraformer/releases/latest | grep tag_name | cut -d '"' -f 4)/terraformer-${PROVIDER}-linux-amd64
chmod +x terraformer-${PROVIDER}-linux-amd64
sudo mv terraformer-${PROVIDER}-linux-amd64 /usr/local/bin/terraformer

#

gcloud iam service-accounts keys create group1-sa-key-file \
--iam-account=group1@group1-6m11.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS=group1-sa-key-file # <file path of the JSON file that contains our service account key>

terraformer import google --regions=us-central1 --projects=group1-6m11 -v

cd generated/google/group1-6m11/
