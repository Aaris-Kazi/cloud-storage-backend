"# cloud-storage-backend" 


## Docker Command to run
    docker build -t cloud_drive:v1.0.7 .

    docker stop drive

    docker rm drive

    docker run -d -p 8000:8000 --name=drive cloud_drive:v1.0.7

    docker run -d \
    --name drive \
    -p 8000:8000 \
    -v /home/warhero/cloud_drive_storage:/app/storage \
    cloud_drive:v1.0.7
