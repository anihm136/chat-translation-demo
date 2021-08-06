# Live Chat Translation Demo
This repository contains the source code and deployment scripts for demonstrating live translation of support chat using Google Cloud Translation

## What does it do?
This demonstration sets up two applications - a standard wordpress blog site, and a support chat application. The wordpress site is configured to display a chat widget, used to access the support chat. The support chat site displays a dashboard to view support requests. A translation service is also set up, which automatically detects the language on either end and performs translation in both directions

## How does it work?
The entire application is deployed as a set of Kubernetes services. The translation service uses the Google Cloud Translation SDK to perform translation, and returns translated content to the clients. The translation service can be configured to use custom models, either for all translations or for specific language pairs

## Setup
Clone the source code to a folder, say `live-chat-demo`. Then, follow the steps in the given order
### Infrastructure
1. [Create](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-zonal-cluster) a new GKE cluster to run the applications
2. [Create](https://cloud.google.com/sql/docs/mysql/create-manage-databases) two new MySQL databases - one for the wordpress installation and one for the chat application
3. If desired, set up separate users for the two databases. Note the usernames, passwords and names of each database
4. Enable private IP access for Cloud SQL. This will allow the Kubernetes nodes to connect to the database using the internal network

### Kubernetes Services
1. Go to `kube_depl/services`. This folder contains YAML configurations to create services for all the components of the application
2. Apply each configuration to create the services
3. Wait for the services to obtain public IP addresses. Note the public IP address for each service

### Building images
1. From the root directory, run `bootstrap.sh` to download and set up the necessary external resources
2. To build the wordpress images, go to `wp_image` and create images using `Dockerfile` and `Dockerfile.bootstrap`. The following commands will create two tags called `latest`, containing the application, and `install`, used for initial setup
```sh
docker build . -f Dockerfile -t wp-custom:latest
docker build . -f Dockerfile.bootstrap -t wp-custom:install
```
3. To build the chat application images, go to `lhc_image` and create images using `Dockerfile` and `Dockerfile.bootstrap`. When creating the application image using `Dockerfile`, the public IP address of the translation service must be passed in as a build argument. The following commands will create two tags called `latest`, containing the application, and `install`, used for initial setup
```sh
docker build . -f Dockerfile -t lhc-custom:latest --build-arg TRANSLATE_SERVICE_URL=<public IP and port of translation service>
docker build . -f Dockerfile.bootstrap -t lhc-custom:install
```
4. To build the translation service image, go to `translate_image` and create an image using `Dockerfile`. No installation step is necessary for this service
```sh
docker build . -t translate-service:latest
```
5. Push all the images to a container registry. [Here](https://cloud.google.com/artifact-registry/docs/docker/quickstart) is a guide on creating a container registry using Google Artifact Registry

### Credentials
1. Enable and set up [workload identity](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine#workload-identity) on the GKE cluster. The YAML config for creating the Kubernetes service account is provided in `kube_depl/config/serviceAccount.yaml`
2. Modify `kube_depl/config/config.yaml` with the public IP addresses of the three services as noted earlier, and apply the configuration
3. Create a copy of `kube_depl/config/env.example`, say `kube_depl/config/env`, and fill in the database credentials as noted earlier
4. Create a secret to hold the credentials - 
```sh
kubectl create secret generic db-credentials --from-env-file kube_depl/config/env
```
5. [Set up](https://cloud.google.com/translate/docs/setup) the Cloud Translation service. Create a service account using IAM with permissions to access the Cloud Translation service, and download the private key file for the service account
6. Create a Kubernetes secret to store the key file and insert it into the translation service
```sh
kubectl create secret generic translate-service-account-key --from-file=key.json=<name of private key file>.json
```

### Install applications
1. Go to `kube_depl/bootstrap`. This folder contains YAML configurations for initial installation of each application. Modify each of the configurations with the path to the images created earlier
2. Install the wordpress application. The default username and password are 'admin' -
```sh
kubectl apply -f kube_depl/bootstrap/wp.yaml
```  
3. The chat application needs to be installed through a web interface. First run the installation job -
```sh
kubectl apply -f kube_depl/bootstrap/lhc.yaml
```
Then, navigate to the public IP address of the chat application service, and follow the instructions to configure database and application credentials

### Run applications
1. Go to `kube_depl/pods`. This folder contains YAML configurations for creating Kubernetes deployments for the applications. Modify each of the configurations with the path of the images created earlier
2. Create deployments for each application -
```sh
kubectl apply -f kube_depl/pods/wp.yaml
kubectl apply -f kube_depl/pods/lhc.yaml
kubectl apply -f kube_depl/pods/translate.yaml
```
3. The applications are now accessible at their respective public IP addresses
