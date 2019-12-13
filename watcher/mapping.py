#Add mapping between manifest fields and BQ fields

def getDBMapping(mappingID, *args):
  finalMapping={}
  if mappingID == 'globalImagePullEvents':
    finalMapping={"manifest" : "bqManifestField", "image_create_date" : "bqImageCreateDate","namespace":"bqNameSpace"}
    #Just add more "nextField":"bqNextFields
  else:
    finalMapping=""

  return finalMapping

