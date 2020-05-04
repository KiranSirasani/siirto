FROM centos:7

RUN yum update -y && yum install sudo -y && yum install yum-utils -y \
    && yum groupinstall development -y && yum install https://centos7.iuscommunity.org/ius-release.rpm -y && yum install python36u -y \
    && yum install python36u-pip -y && yum install python36u-devel -y

WORKDIR /app

COPY minioexport ./minioexport
COPY dockerfile .
COPY setup.py .
COPY start_minio_to_nfs.sh .

RUN pip3 install wheel
RUN python3.6 setup.py bdist_wheel
RUN pip3 install dist/*

RUN ["chmod", "+x", "./start_minio_to_nfs.sh"]
ENTRYPOINT ["/bin/bash", "-c", "./start_minio_to_nfs.sh \"$@\"", "--"]
