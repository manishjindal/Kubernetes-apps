# Kubernetes Helm

You can follow below links to install helm on your system or you can go to installation directly.

[https://github.com/kubernetes/helm]( https://github.com/kubernetes/helm )

[https://docs.helm.sh/using_helm/#installing-helm ]( https://docs.helm.sh/using_helm/#installing-helm ) 

## Installation

```$xslt
wget https://kubernetes-helm.storage.googleapis.com/helm-v2.8.2-linux-amd64.tar.gz

tar -zxvf helm-v2.8.2-linux-amd64.tar.gz

mv linux-amd64/helm /usr/local/bin/helm
```

you can download specific version of helm from [here](https://github.com/kubernetes/helm/releases)


## Create Service Account

Create service account using following configuration.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: tiller-clusterrolebinding
subjects:
- kind: ServiceAccount
  name: tiller
  namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: ""
```

## Init Tiller

```
helm init --service-account tiller --upgrade
```

