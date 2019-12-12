from kubernetes import client, config, watch

#Add mapping between manifest fields and BQ fields
BQ_MAPPING={"manifest" : "bqManifestField", 
            "image_create_date" : "bqImageCreateDate",
            "namespace":"bqNameSpace"
            #,"nextField":"bqNextField"
            }


def getManifestData(image, *args):
  #Use image name to get manifest data
  #Use args to request specific data from manifest

  #Build URL to registry, repo/image, and tag

  #Get SHA, Get Image Create Date


  ### TEST DATA ###
  manifestData = {"manifest":"sha14147104",
                  "image_create_date":"12-12-19 10:00:00 AM",
                  "namespace":"madeupnamespace"
                  #,"nextField":"test11"
                  }
  
  #Return dict
  return manifestData


def constructData(imageName, imagePullDate, manifestData, **kwargs):
  #Uses manifestData and field mappings from kwargs to construct data as BQ needs it.
  
  newPair={}
  finalPair={}

  for key in manifestData:
      #print("key: %s , value: %s" % (key, bigQueryData[key]))
    mfstField = key

    #loop through kwargs to find bqFieldname from manifest fieldName
    for key, value in kwargs.items():
      if key == mfstField:
        print("%s\t" % "Field Mapping Found: " + mfstField + "to:" + value)
        bqField = value
        bqValue = manifestData[key]
   
        newPair = {bqField:bqValue}

        finalPair[key] = manifestData[key]

    print("%s\t" % "KeyValue added: " + str(newPair))

  print("%s\t" % "Final KeyValues: " + str(finalPair))

  bigQueryData = finalPair

  #Add regular Args, probably do this to original dict
  bigQueryData['bqImageName'] = imageName
  bigQueryData['bqImagePullDate'] = str(imagePullDate)

  return bigQueryData



def insertData(bigQueryData, **kwargs):
  #Inserts data into BQ

  #Connect to BQ

  #Need more data formatting?
  
  fields=""
  values=""
  commaHelper=0

  for key in bigQueryData:
    #print("key: %s , value: %s" % (key, bigQueryData[key]))
    if commaHelper==0:
      fields = key
      values = bigQueryData[key]
    else:
      fields = fields + ", " + key
      values = values + ", " + bigQueryData[key]
    commaHelper += 1

  print("%s\t\t" % "Parsed Fields: " + fields)
  print("%s\t\t" % "Parsed Values: " + values)

  #Build insert statement, u the data structure created previously.
  INSERT_STATEMENT = "INSERT INTO biqQueryTable (" + fields + ") VALUES (" + values + ")"
  
  #Execute Insert Statement
  print("%s\t" % "Test Insert Statement: " + INSERT_STATEMENT)
  print()



def listPullEvents():
  #No watching.  Pulls anything in resource.  May not be neccessary since watch pulls history too?
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


def watchPullEvents():
  #Watches events.  I believe this also pulls whatever is in resource.
  v1 = client.CoreV1Api()

  #Counters (just used to stop a runaway train and look at noise) - can remove.
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
        print("%s\t" % "Test ImageName: " + imageName)

        #Use EventLastTimestamp for ImagePullDate
        imagePullDate = event['object'].last_timestamp
        print("%s\t" % "Test ImagePullDate: " + str(imagePullDate))

        #Get Manifest Data (SHA, ImageCreateDate,etc.)
        testManifestData = getManifestData(imageName,'manifest','image_create_date')
        print("%s\t" % "Test Manifest Data: " + str(testManifestData))

        #Construct Data to match BQ. Uses BQ_MAPPING Kwarg set at top. Should be config.
        testBiqQueryData = constructData(imageName, imagePullDate, testManifestData,**BQ_MAPPING)
        print("%s\t" % "Test BiqQuery Data: " + str(testBiqQueryData))

        #Insert data into BQ.
        insertData(testBiqQueryData)

        if countImagePullEventsCurrent == countImagePullEventsMax:
            w.stop()
        countImagePullEventsCurrent += 1

      if countAllEventsCurrent == countAllEventsMax:
          w.stop()
      print("Event Counter: "+ str(countAllEventsCurrent) + " (" + event['object'].reason + ")")
      countAllEventsCurrent += 1

  print("%s\t" % "Finished Event Stream.")



def main():
 
  config.load_kube_config()

  watchPullEvents()


if __name__ == '__main__':
    main()