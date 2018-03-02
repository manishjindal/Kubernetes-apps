# Etcd Helm Chart

Credit to https://github.com/ingvagabund. This is an implementation of that work

* https://github.com/kubernetes/contrib/pull/1295

## Prerequisites Details
* Kubernetes 1.5 (for `StatefulSets` support)
* PV support on the underlying infrastructure

## StatefulSet Details
* https://kubernetes.io/docs/concepts/abstractions/controllers/statefulsets/

## StatefulSet Caveats
* https://kubernetes.io/docs/concepts/abstractions/controllers/statefulsets/#limitations

## Todo
* Implement SSL, increase replica number.

## Chart Details
This chart will do the following:

* Implement an etcd cluster using Kubernetes StatefulSets
* Does not support etcd v3.2.x

## Configuration

The following tables lists the configurable parameters of the etcd chart and their default values.

| Parameter               | Description                        | Default                                                    |
| ----------------------- | ---------------------------------- | ---------------------------------------------------------- |
| `Name`                  | Spark master name                  | `etcd`                                                     |
| `Image`                 | Container image name               | `docker.mot-solutions.com/msi/etcd`                      |
| `ImageTag`              | Container image tag                | `v3.1.10`                                                    |
| `ImagePullPolicy`       | Container pull policy              | `Always`                                                   |
| `Replicas`              | k8s statefulset replicas   Currently only 1 is possible        | `1`                                                        |
| `Component`             | k8s selector key                   | `etcd`                                                     |
| `Cpu`                   | container requested cpu            | `100m`                                                     |
| `Memory`                | container requested memory         | `512Mi`                                                    |
| `ClientPort`            | k8s service port                   | `2379`                                                     |
| `PeerPorts`             | Container listening port           | `2380`                                                     |
| `Storage`               | Persistent volume size             | `1Gi`                                                      |
| `StorageClass`          | Persistent volume storage class    | `anything`                                                 |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```bash
$ helm install --name my-release -f values.yaml etcd
```

> **Tip**: You can use the default [values.yaml](values.yaml)

# Deep dive

## Cluster Health

```
$ for i in <0..n>; do kubectl exec <release-podname-$i> -- sh -c 'etcdctl cluster-health'; done
```
eg.
```
$ for i in {0..9}; do kubectl exec named-lynx-etcd-$i --namespace=etcd -- sh -c 'etcdctl cluster-health'; done
member 7878c44dabe58db is healthy: got healthy result from http://named-lynx-etcd-7.named-lynx-etcd:2379
member 19d2ab7b415341cc is healthy: got healthy result from http://named-lynx-etcd-4.named-lynx-etcd:2379
member 6b627d1b92282322 is healthy: got healthy result from http://named-lynx-etcd-3.named-lynx-etcd:2379
member 6bb377156d9e3fb3 is healthy: got healthy result from http://named-lynx-etcd-0.named-lynx-etcd:2379
member 8ebbb00c312213d6 is healthy: got healthy result from http://named-lynx-etcd-8.named-lynx-etcd:2379
member a32e3e8a520ff75f is healthy: got healthy result from http://named-lynx-etcd-5.named-lynx-etcd:2379
member dc83003f0a226816 is healthy: got healthy result from http://named-lynx-etcd-2.named-lynx-etcd:2379
member e3dc94686f60465d is healthy: got healthy result from http://named-lynx-etcd-6.named-lynx-etcd:2379
member f5ee1ca177a88a58 is healthy: got healthy result from http://named-lynx-etcd-1.named-lynx-etcd:2379
cluster is healthy
```


Once a replica is terminated (either by running ``kubectl delete pod etcd-ID`` or scaling down),
content of ``/var/run/etcd/`` directory is cleaned up.
If any of the etcd pods restarts (e.g. caused by etcd failure or any other),
the directory is kept untouched so the pod can recover from the failure.
