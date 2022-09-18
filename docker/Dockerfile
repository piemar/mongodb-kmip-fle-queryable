FROM ubuntu:18.04


# Install required gnupg package
RUN apt-get update && apt-get -y install gnupg

RUN apt-get update && \
    apt-get -qy full-upgrade && \
    apt-get install -qy curl     

# Install required ca-certificates to prevent the error in the certificate verification
RUN apt-get -y install jq
RUN apt-get -y install ca-certificates && update-ca-certificates
RUN apt install -y lsb-core
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
RUN apt install -y software-properties-common
RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
# Import the public key used by the package management system
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN apt-get update && apt-get -y install vault
# Create a list file for MongoDB
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list

# Reload local package database
RUN apt-get update
# Install the MongoDB packages
RUN apt-get -y install mongodb-org-shell
RUN apt-get -y install mongodb-org-tools


RUN \
# Update
apt-get update -y && \
# Install Unzip
apt-get install unzip -y && \
# need wget
apt-get install wget -y && \
# vim
apt-get install vim -y

################################
# Install python
################################

RUN apt-get install -y python3-pip
#RUN ln -s /usr/bin/python3 python
#RUN pip3 install --upgrade pip
#RUN python3 -V
#RUN pip3 install dnspython
#RUN pip3 install pykmip
#RUN pip3 install pymongo
#RUN pip3 install pymongocrypt 
RUN echo 'tzdata tzdata/Areas select Europe' | debconf-set-selections
RUN echo 'tzdata tzdata/Zones/Europe select Paris' | debconf-set-selections
RUN DEBIAN_FRONTEND="noninteractive" apt install -y tzdata
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.com/apt/ubuntu bionic/mongodb-enterprise/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-enterprise.list
RUN apt-get update
RUN apt-get install -y -q mongodb-enterprise
RUN curl https://releases.hashicorp.com/vault/1.10.0-rc1+ent/vault_1.10.0-rc1+ent_linux_arm64.zip --output vault-ent.zip 
RUN unzip -qq vault-ent.zip
RUN cp vault /usr/bin/vault
RUN rm vault-ent.zip
RUN export VAULT_ADDR=http://127.0.0.1:8200
RUN add-apt-repository --yes ppa:deadsnakes/ppa
RUN apt install -y python3.8
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install pymongo
RUN python3.8 -m pip install dnspython
RUN python3.8 -m pip install pykmip
RUN python3.8 -m pip install pymongocrypt 
RUN mkdir /csfle_shared_lib
COPY mongo_crypt_v1.so /csfle_shared_lib/mongo_crypt_v1.so