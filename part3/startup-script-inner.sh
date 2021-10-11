#!/bin/bash

# # [START startup_script]
# apt-get update
# apt-get -y install imagemagick

# # Use the metadata server to get the configuration specified during
# # instance creation. Read more about metadata here:
# # https://cloud.google.com/compute/docs/metadata#querying
# IMAGE_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "Metadata-Flavor: Google")
# TEXT=$(curl http://metadata/computeMetadata/v1/instance/attributes/text -H "Metadata-Flavor: Google")
# CS_BUCKET=$(curl http://metadata/computeMetadata/v1/instance/attributes/bucket -H "Metadata-Flavor: Google")

# mkdir image-output
# cd image-output
# wget $IMAGE_URL
# convert * -pointsize 30 -fill white -stroke black -gravity center -annotate +10+40 "$TEXT" output.png

# # Create a Google Cloud Storage bucket.
# gsutil mb gs://$CS_BUCKET

# # Store the image in the Google Cloud Storage bucket and allow all users
# # to read it.
# gsutil cp -a public-read output.png gs://$CS_BUCKET/output.png

sudo apt-get update
sudo apt-get install -y python3 python3-pip git
mkdir flask
git clone https://github.com/pallets/flask.git flask
cd /flask/examples/tutorial
sudo python3 setup.py install
sudo pip3 install -e .

export FLASK_APP=flaskr
flask init-db
nohup flask run -h 0.0.0.0 &

# [END startup_script]

