# Live Chat Translation Demo
This repository contains the source code and deployment scripts for demonstrating live translation of support chat using Google Cloud Translation

## What does it do?
This demonstration sets up two applications - a standard wordpress blog site, and a support chat application. The wordpress site is configured to display a chat widget, used to access the support chat. The support chat site displays a dashboard to view support requests. A translation service is also set up, which automatically detects the language on either end and performs translation in both directions

## How does it work?
The entire application is deployed as a set of Kubernetes services. The translation service uses the Google Cloud Translation SDK to perform translation, and returns translated content to the clients. The translation service can be configured to use custom models, either for all translations or for specific language pairs

## Setup
Clone the source code to a folder, say `live-chat-demo`. Then, follow the steps in the given order
### Database
1. [Create](https://cloud.google.com/sql/docs/mysql/create-manage-databases) two new MySQL databases - one for the wordpress installation and one for the chat application
2. If desired, set up separate users for the two databases. Note the usernames, passwords and names of each database
3. Enable private IP access for Cloud SQL. This will allow the Kubernetes nodes to connect to the database using the internal network

### Kubernetes Services
1. Go to `kube_depl/services`. This folder contains YAML configurations to create services for all the components of the application
2. Apply each configuration to create the services
3. Wait for the services to obtain public IP addresses. Note the public IP address for each service

### Credentials
1. Enable and set up [workload identity](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine#workload-identity). The YAML config for creating the Kubernetes service account is provided in `kube_depl/config/serviceAccount.yaml`
2. Modify `kube_depl/config/config.yaml` with the public IP addresses of the three services as noted earlier, and apply the configuration
3. Create a copy of `kube_depl/config/env.example`, say `kube_depl/config/env`, and fill in the database credentials as noted earlier
4. Create a secret to hold the credentials - 
```sh
kubectl create secret generic db-credentials --from-env-file kube_depl/config/env
```

### Install applications
1. Go to `kube_depl/bootstrap`. This folder contains YAML configurations for initial installation of each application
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
1. Go to `kube_depl/pods`. This folder contains YAML configurations for creating Kubernetes deployments for the applications
2. Create deployments for each application -
```sh
kubectl apply -f kube_depl/pods/wp.yaml
kubectl apply -f kube_depl/pods/lhc.yaml
kubectl apply -f kube_depl/pods/translate.yaml
```
3. The applications are now accessible at their respective public IP addresses
