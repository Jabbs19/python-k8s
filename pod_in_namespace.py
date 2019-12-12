from kubernetes import client, config

config.load_kube_config()

namespace='default'
v1=client.CoreV1Api()
print("Listing pods with their Images:")
ret = v1.list_namespaced_pod_template(namespace,watch=False)
for i in ret.items:
    print(ret)
    
    #containers = i.spec.containers

    #single_id = image_id[0].image

    #container_count = range(len(containers))
    #print(single_id)
    #print(container_count)
    #for j in container_count:

      #print("Conatiner:" )
#      single_id = containers[j].image
      #print("%s\t%s\t%s\t%s" % (single_id, i.spec.containers.name, i.metadata.namespace, i.metadata.name))
 #     print("%s\t%s\t%s" % ( i.metadata.namespace, i.metadata.name, single_id,))

  #    j = j + 1
      #print(j)
      #print(image_id[j].image)
      

    #  single_id = image_id[j].image
     # print(single_id)
     # j = j + 1
    #print("%s\t%s\t%s" % (for j in image_id: print("%s" % j.image_id), i.spec.containers, i.metadata.namespace, i.metadata.name))