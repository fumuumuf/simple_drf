FROM centos:centos7
RUN yum update -y \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum -y groupinstall 'Development tools'

RUN yum install -y mysql \
        mysql-devel \
        mysql-server \
        gcc \
        make \
        git \
        openssl-devel \
        sqlite-devel \
        vim \
        which \
        graphviz-devel \
        libxslt \
        python36u python36u-libs python36u-devel python36u-pip

# lang
RUN yum -y reinstall glibc-common
RUN localedef -v -c -i ja_JP -f UTF-8 ja_JP.UTF-8; echo "";
ENV LANG=ja_JP.UTF-8

# 日本語フォント追加
RUN curl -L -O https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip \
 && unzip -d noto NotoSansCJKjp-hinted.zip \
 && mkdir -p /usr/share/fonts/opentype \
 && mv -fv noto /usr/share/fonts/opentype/noto \
 && rm -rfv NotoSansCJKjp-hinted.zip \
 && fc-cache -fv \
 && chmod -Rf a+r /usr/share/fonts/*

# install python3
RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 50 \
    && alternatives --install /usr/bin/pip3 pip /usr/bin/pip3.6 50

WORKDIR /var/www/django

COPY apps/requirements.txt requirements.txt

ADD ./apps /var/www/django

# venv environment
ENV HOME=/root
ENV VENV_PATH=${HOME}/.venv
RUN python3 -m venv ${VENV_PATH}
ENV PATH=${VENV_PATH}/bin:${PATH}

# install python packages
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE 8000
