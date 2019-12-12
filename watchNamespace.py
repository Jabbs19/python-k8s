from kubernetes import client, config, watch

#Add mapping between manifest fields and BQ fields
BQ_MAPPING={"manifest" : "bqManifestField", 
            "image_create_date" : "bqImageCreateDate",
            "namespace":"bqNameSpace"}


def getManifestData(image, *args):
  #Use image name to get manifest data
  #Use args to request specific data from manifest

  #Build URL to registry, repo/image, and tag

  #Get SHA, Get Image Create Date

  #Return dict
  manifestData = {"manifest":"sha14147104","image_create_date":"12-12-19 10:00:00 AM","namespace":"madeupnamespace"}
  return manifestData


def constructData2(imageName, imagePullDate, manifestData, **kwargs):
  #with manifestData, build BQ data structure
  #Might need kwargs to tell it how to format/map Biq Query fields with manifest fields and values.
  parseManifest = manifestData['manifest']
  parseImageCreateDate = manifestData['image_create_date']
  parseImageName = imageName
  parseImagePullDate = str(imagePullDate)
  
  newPair={}
  finalPair={}
  first=0
  for key in manifestData:
      #print("key: %s , value: %s" % (key, bigQueryData[key]))
    bqField = key
    bqValue = manifestData[key]
    newPair = {bqField:bqValue}

    if first==0:
      finalPair = newPair
    else:
      finalPair[key] = manifestData[key]
      #finalPair = finalPair.update(newPair)

    print("%s\t" % "Test KeyPair: " + str(newPair))
    first = first + 1

  print("%s\t" % "Final KeyPair: " + str(finalPair))
  bigQueryData = {"bqManifestField":parseManifest,"bqImageCreateDate":parseImageCreateDate,"bqImageName":parseImageName,"bqImagePullDate":parseImagePullDate}
  return bigQueryData

def constructData(imageName, imagePullDate, manifestData, **kwargs):
  #with manifestData, build BQ data structure
  #Might need kwargs to tell it how to format/map Biq Query fields with manifest fields and values.
  parseManifest = manifestData['manifest']
  parseImageCreateDate = manifestData['image_create_date']
  parseImageName = imageName
  parseImagePullDate = str(imagePullDate)
  
  newPair={}
  finalPair={}
  first=0
  for key in manifestData:
      #print("key: %s , value: %s" % (key, bigQueryData[key]))
    mfstField = key

    #loop through kwargs to find bqFieldname from manifest fieldName
    for key, value in kwargs.items():
      if key == mfstField:
        print("%s\t\t" % "Mapping Found: " + mfstField + "to:" + value)
        bqField = value
        bqValue = manifestData[key]
   
        newPair = {bqField:bqValue}

        finalPair[key] = manifestData[key]

    print("%s\t" % "KeyValue added: " + str(newPair))
    #print("Test KeyPair: " + str(newPair))
    first = first + 1

  print("%s\t" % "Final KeyValues: " + str(finalPair))
  #bigQueryData = {"bqManifestField":parseManifest,"bqImageCreateDate":parseImageCreateDate,"bqImageName":parseImageName,"bqImagePullDate":parseImagePullDate}
  bigQueryData = finalPair
  #Add regular Args, probably do this to original dict
  bigQueryData['bqImageName'] = imageName
  bigQueryData['bqImagePullDate'] = str(imagePullDate)

  return bigQueryData

def insertData(bigQueryData, **kwargs):
  #Insert data into BQ

  #Connect to BQ

  #Need more data formatting?
  
  fields=""
  values=""
  comma=0

  for key in bigQueryData:
    #print("key: %s , value: %s" % (key, bigQueryData[key]))
    if comma==0:
      fields = key
      values = bigQueryData[key]
    else:
      fields = fields + ", " + key
      values = values + ", " + bigQueryData[key]
    comma = comma + 1

  print("%s\t\t" % "Test Fields: " + fields)
  print("%s\t\t" % "Test Values: " + values)

  #Build insert statement
    #Using the data structure created previously, build the insert statement
  INSERT_STATEMENT = "INSERT INTO biqQueryTable (" + fields + ") VALUES (" + values + ")"
  print("%s\t" % "Test Insert Statement: " + INSERT_STATEMENT)
  print()



def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    v1 = client.CoreV1Api()
    #v1= client.V1Container()
    countAllEventsMax = 1000
    countAllEventsCurrent = 1
    countImagePullEventsMax = 100
    countImagePullEventsCurrent = 1

    w = watch.Watch()
    for event in w.stream(v1.list_event_for_all_namespaces):
    #for event in w.stream(v1.list_event_for_all_namespaces, timeout_seconds=100):
        #if event['object'].involved_object.kind == "Pod":
        if event['object'].reason == "Pulled":
          print()
          print("##### IMAGE PULL EVENT (" + str(countImagePullEventsCurrent) +") FOUND ####")
          #Parse the "message" for imagename
          imageNameRaw = event['object'].message
          startIndex = imageNameRaw.find('\"') + 1
          stopIndex = imageNameRaw.find('\"',startIndex+1)
          imageName = imageNameRaw[startIndex:stopIndex]

          imagePullDate = event['object'].last_timestamp

          print("%s\t" % "Test ImageName: " + imageName)
          print("%s\t" % "Test ImagePullDate: " + str(imagePullDate))


          testManifestData = getManifestData(imageName,'manifest','image_create_date')
          print("%s\t" % "Test Manifest Data: " + str(testManifestData))

          #set BQ map structure
         # BQ_MAPPING={"manifest" : "bqManifestField", "image_create_date" : "bqImageCreateDate"}
          testBiqQueryData = constructData(imageName, imagePullDate, testManifestData,**BQ_MAPPING)
          print("%s\t" % "Test BiqQuery Data: " + str(testBiqQueryData))

          insertData(testBiqQueryData)

          if countImagePullEventsCurrent == countImagePullEventsMax:
              w.stop()
       	  countImagePullEventsCurrent += 1

        if countAllEventsCurrent == countAllEventsMax:
            w.stop()
        print("Event Counter: "+ str(countAllEventsCurrent) + " (" + event['object'].reason + ")")
        countAllEventsCurrent += 1

    print("%s\t" % "Finished Event Stream.")


if __name__ == '__main__':
    main()