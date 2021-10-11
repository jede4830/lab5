#!/bin/bash
#!/usr/bin/python
apt-get update
#apt-get -y install imagemagick

IMAGE_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "Metadata-Flavor: Google")
TEXT=$(curl http://metadata/computeMetadata/v1/instance/attributes/text -H "Metadata-Flavor: Google")
CS_BUCKET=$(curl http://metadata/computeMetadata/v1/instance/attributes/bucket -H "Metadata-Flavor: Google")
mkdir image-output
cd image-output
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/jede4830/lab5
echo "Came to startup script"
echo "printed the version"
sudo pip3 install --upgrade google-api-python-client
sudo pip3 install --upgrade google-api-python-client oauth2client
#cd lab5
cd lab5/part3
export SERVICE_CREDENTIALS=$(curl http://metadata/computeMetadata/v1/instance/attributes/service-credentials -H "Metadata-Flavor: Google")
echo $SERVICE_CREDENTIALS | tee service-credentials.json
sudo python3 part3a.py 'dulcet-order-323902' 'lab5vminstance'
echo "Run python file"


