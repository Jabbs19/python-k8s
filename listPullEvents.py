from kubernetes import client, config

def main():

  config.load_kube_config()

  v1=client.CoreV1Api()
  print("Listing pods with their Images:")
  ret = v1.list_event_for_all_namespaces(watch=False)
  for i in ret.items:
    if i.reason == "Pulled":
      print()
      print("##### IMAGE PULL EVENT FOUND ####")

      #Parse the "message" for imagename
      imageNameRaw = i.message
      startIndex = imageNameRaw.find('\"') + 1
      stopIndex = imageNameRaw.find('\"',startIndex+1)
      imageName = imageNameRaw[startIndex:stopIndex]
      print("%s\t" % "Test ImageName: " + imageName)

      #Use EventLastTimestamp for ImagePullDate
      imagePullDate = i.last_timestamp
      print("%s\t" % "Test ImagePullDate: " + str(imagePullDate))
      
      #Parse the "message" for imagename
            #imageNameRaw = event['object'].message
            #startIndex = imageNameRaw.find('\"') + 1
            #stopIndex = imageNameRaw.find('\"',startIndex+1)
            #imageName = imageNameRaw[startIndex:stopIndex]
            #print("%s\t" % "Test ImageName: " + imageName)
      #print(i)

if __name__ == '__main__':
    main()  
