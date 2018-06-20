import boto3
import json
import os
from common.logger_utility import *
from boto3.dynamodb.conditions import Attr, Key
from common.constants import *

class ManifestHandler:

    def __get_manifests_to_process(self,event, context):
        try:
            batch_id=event.get("BatchId")
            data = {}
            data["jamurl"]=""
            data["alerturl"]=""
            data["irregularityurl"]=""
            data["irregularity_alerturl"]=""
            data["irregularity_jamurl"]=""
            data["irregularity_point_sequenceurl"]=""
            data["jam_point_sequenceurl"]=""
            data["queueUrl"]=event.get("queueUrl")
            data["receiptHandle"]=event.get("receiptHandle")
            if batch_id is None:
                return data
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('dev-CurationManifestFilesTable')
            response = table.query(
                       IndexName="dev-BatchId-TableName-index",
                        KeyConditionExpression=Key('BatchId').eq(batch_id),
                        FilterExpression=Attr('FileStatus').eq('open'))
          
            data["batchId"]=batch_id
            for item in response['Items']:
                            manifest_s3key_name = item['ManifestS3Key']
                            url=item["TableName"]+"url"
                            data[url] = item["ManifestS3Key"]
                            totalCuratedRecordsByState=item["TotalCuratedRecordsByState"]
            
            
            return data
        except Exception as e:
            LoggerUtility.logError("Error getting manifests for batches")
            raise e
    
    def get_manifests(self, event, context):
        return self.__get_manifests_to_process(event, context)
        