# Flaskapp for minikube

Running python flask app which shows the POD-ID where application is running

#### Getting Started

##### First we will use some other image for deployment than we will update that deployment to use this image.

###### Make Deployment with other image-
```
kubectl.exe run myflaskapp-forminikube --image=docker.io/mjindal/myflaskapp-forminikube:latest --port=5000
```
###### Expose Deployment
```
kubectl expose deployment/myflaskapp-forminikube --type="NodePort" --port 5000
```

###### View Deployment from host system (this will give the url where it is running)
```
minikube.exe service myflaskapp-forminikube --url
```
you should see the container id where app is running .

###### Now scale application to use 5 containers
```
kubectl.exe scale deployment myflaskapp-forminikube --replicas 5
```
Refresh the browser you should see different-different container id.

###### There should be exactly 5 pods running -
```
kubectl.exe get pods
```

###### Scale down replica to 1 - 4 pods should die immediately !
```
kubectl.exe scale deployment myflaskapp-forminikube --replicas 1
```
###### Now change the image
```
kubectl set image deployments/myflaskapp-forminikube myflaskapp-forminikube=mjindal/myflaskapp:latest
```
##### Prerequisites

What things you need to install the software and how to install them

```
Download kubectl and minikube.
Extract both in one folder and add the folder in path.

```

##### Installation

A step by step series of examples that tell you have to get a development env running

Install minikube

* [minikube](https://github.com/kubernetes/minikube/releases)


Install Kubectl

* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)


Start Minikube

```
export PATH = $PATH:installation_dir
minikube start

```