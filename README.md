# Deploy FastAPI Scikit-learn Microservice on AWS EC2


You can watch this video tutorial > [link tutorial YOUTUBE](https://youtu.be/hmAJKgMIyCk "link tutorial")


**install dependencies Python**

    $ python -m venv venv
    $ source venv/scripts/activate | ./venv/scripts/activate
    $ pip install -r ml_service/requirements.txt
    $ pip install -r registry_service/requirements.txt

**testing run server on localhost ml port 8001**

    $ cd ml_service
    $ uvicorn app.main:app --port 8001 --reload

**testing run server on localhost registry port 8002**

    $ cd registry_service
    $ uvicorn app.main:app --port 8002 --reload

**Run docker container swarm**

    $ docker compose up -d

**You can run reverse proxy this url**

    https://localhost:80/api/v1/registry/docs
    https://localhost:80/api/v1/ml/docs

**Access to SSH Client EC2**

    1. Open an SSH client.
    2. Locate your private key file. The key used to launch this instance is nginx_key.pem
    3. Run this command, if necessary, to ensure your key is not publicly viewable.
        chmod 400 [you key pair accss]
    4. Connect to your instance using its Public DNS:
        [your public DNS]

    Example:
     ssh -i "fastapi_key.pem" ubuntu@123-456.987.compute-1.amazonaws.com

**Setup install dependencies instance**
    
    $ sudo apt-get update
    $ sudo apt install -y python3-pip nginx
    $ sudo apt install docker.io
    $ sudo apt install docker-compose

**Setup Nginx**
    
    $ sudo /etc/nginx/sites-enabled/fastapi_nginx.conf

```nginx
server {
  listen 8080;
   server_name [your domain];

  location / {
    proxy_pass http://127.0.0.1:8001;
  }

  location /api/v1/ml {
    proxy_pass http://127.0.0.1:8001/api/v1/ml;
  }

  location /api/v1/registry {
    proxy_pass http://127.0.0.1:8002/api/v1/registry;
  }

  location /api/v1/authenticate {
    proxy_pass http://127.0.0.1:8002/api/v1/authenticate;
  }

}
```

**Push stack container**
    
    $ git clone https://github.com/watcharap0n/deploy-fastapi-linear-ec2.git
    $ cd deploy-fastapi-linear-ec2
    $ sudo docker-compose up -d
    $ curl -s localhost:8001 | "result"

**open your domain :)** ..







