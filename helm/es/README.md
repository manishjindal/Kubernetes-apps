# Elasticsearch Helm Chart

## StatefulSets Details
* https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

## StatefulSets Caveats
* https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#limitations

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add msi http://location_of_Helm_repository
$ helm install --name my-release elasticsearch
```

## Deleting the Charts

Delete the Helm deployment as normal

```
$ helm delete my-release
```

Deletion of the StatefulSet doesn't cascade to deleting associated PVCs. To delete them:

```
$ kubectl delete pvc -l release=my-release,component=elasticsearch
```

## Configuration

The following tables lists the configurable parameters of the elasticsearch chart and their default values.

| Parameter                                  | Description                              | Default                                            |
| ------------------------------------------ | ---------------------------------------- | -------------------------------------------------- |
| `common.image.repository`                  | Container image name                     | `docker.mot-solutions.com/msi/elasticsearch`       |
| `common.image.tag`                         | Container image tag                      | `testkubernetes`                                   |
| `common.image.pullPolicy`                  | Container pull policy                    | `IfNotPresent`                                     |
| `common.image.pullSecret`                  | Container image secret name              | `msipull`                                          |
| `elasticsearch.replicas`                   | Elasticsearch node replicas (StatefulSet)| `3`                                                |
| `elasticsearch.storage.size`               | Elasticsearch persistent volume size     | `200Gi`                                            |
| `elasticsearch.storage.class`              | Elasticsearch persistent volume Class    | `portworx`                                         |
| `elasticsearch.env.NUMBER_OF_MASTERS`      | Elasticsearch cluster's quorum size      | `2`                                                |
| `elasticsearch.env.ES_JAVA_OPTS`           | Elasticsearch JAVA heap size             | `-Xms3g -Xmx3g`                                    |
| `resource.limits.memory`                   | Elasticsearch node memory limits         | `6Gi`                                              |
| `resource.limits.cpu`                      | Elasticsearch node cpu limits            | `1000m`                                            |
| `resource.requests.memory`                 | Elasticsearch node memory requests       | `5Gi`                                              |
| `resource.requests.cpu`                    | Elasticsearch node cpu requests          | `500m`                                             |
| `service.annotations.prometheus.io/scrape` | Elasticsearch should be scrapped         | `true`                                             |
| `service.annotations.prometheus.io/path`   | Elasticsearch url to be scrapped at      | `/_prometheus/metrics`                             |
| `service.annotations.prometheus.io/port`   | Elasticsearch port to be scrapped at     | `9200`                                             |
| `sysctl.image.repository`                  | sysctl image name                        | `docker.mot-solutions.com/msi/debian`              |
| `sysctl.image.tag`                         | sysctl image tag                         | `dev-latest`                                       |
| `sysctl.image.pullPolicy`                  | sysctl pull policy                       | `IfNotPresent`                                     |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Note that the sysctl image is used during initialization to run the command `sysctl -w vm.max_map_count=262144`.

In terms of Memory resources you should make sure that you follow that equation:

- `HeapSize < MemoryRequests < MemoryLimits`
