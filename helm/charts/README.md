helm init --service-account tiller --upgrade


## Gitlab Kubernetes

Create service account using "gitlab.yml"

```
kubectl create -f gitlab.yml
````

This will create service account in gitlab-managed-apps namespace 

<img src="https://github.com/manishjindal/Kubernetes-apps/blob/master/helm/charts/images/gitlab-k8s.PNG" width="800">

```
[root@node1 charts]# kubectl get serviceaccount --namespace=gitlab-managed-apps
NAME      SECRETS   AGE
default   1         1h
```

Get the ca.crt and token from this service account and use in gitlab
