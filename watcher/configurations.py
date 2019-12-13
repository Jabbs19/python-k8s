#default values
debugMode=True


def getDBMapping(mappingID, *args):
  #Add mapping between manifest fields and BQ fields
  finalMapping={}
  if mappingID == 'globalImagePullEvents':
    finalMapping={"manifest" : "bqManifestField", "image_create_date" : "bqImageCreateDate","namespace":"bqNameSpace"}
    #Just add more "nextField":"bqNextFields
  else:
    finalMapping=""

  return finalMapping

