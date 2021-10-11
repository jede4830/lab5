import argparse
import os
import time
import googleapiclient.discovery
from six.moves import input
from pprint import pprint
from googleapiclient import discovery
import google.auth
from oauth2client.client import GoogleCredentials


creds, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=creds)
project = 'dulcet-order-323902'
zone = 'us-west1-b'
disk = 'demo-instance'
bucket = 'finley_testbucket5'
startupscript = 'startup-script.sh'

snapshot_body = {
    'name' : 'base-snapshot-demoinstance'
}


def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(project=project, zone=zone, operation=operation['name']).execute()
        print(result)
        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)


def create_instance(compute,project,zone,name,bucket,snapshotname): 
    getsourceSnapshot = compute.snapshots().get(project = project , snapshot = snapshotname).execute()
    source_snapshot = getsourceSnapshot['selfLink']
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(os.path.join(os.path.dirname(__file__), startupscript), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"
    config = {
        'name': name,
        'machineType': machine_type,
        # Specify the boot disk and the image to use as a source.
        'disks': [{
            'boot': True,
            'autoDelete': True,
            'initializeParams': {
                'sourceSnapshot': source_snapshot
            }
        }],
        # Specify a network interface with NAT to access the public internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}]
        }],
        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to pass configuration from deployment scripts to instances.
        'metadata': {
            # Startup script is automatically executed by the instance upon startup.
            'items': [{'key': 'startup-script','value': startup_script}, 
                {'key': 'url','value': image_url}, 
                {'key': 'text','value': image_caption}, 
                {'key': 'bucket','value': bucket}
            ]}
    }
    return compute.instances().insert(project=project, zone=zone, body=config).execute()


def main():
    request = service.disks().createSnapshot(project=project, zone=zone ,disk=disk ,body=snapshot_body)
    response = request.execute()
    time_list = []
    #name1 = 'demo1'
    #name2 = 'demo2'
    #name3 = 'demo3'
    names = ['demo1','demo2','demo3']

    for i in range(0,3):
        t = time.time()
        name = names[i]
        operation = create_instance(service,project,zone,names[i],bucket,snapshot_body['name'])
        wait_for_operation(service,project,zone,operation)
        time_list.append( time.time() - t)

    print(time_list)
    with open('TIMING.md','w') as f:
        for item in time_list:
            f.write("%s\n" % item)


if __name__=='__main__':
    main()


