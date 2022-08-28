FROM ubuntu:latest

# apt init
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl wget automake libtool

# java stuff
RUN apt-get install -y openjdk-8-jdk

# python stuff
RUN apt-get install -y python3-pip python3-dev
RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    ln -s /usr/bin/pip3 pip && \
    pip3 install --upgrade pip

# apt cleanse
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# timezone
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# getting environment variable on console
ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# copying local file into container's /code/ directory
COPY ./requirements.txt /code/requirements.txt

# python configuration
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

# copying the rest of the files into container's /code/ directory
# container's working directory is /code/
COPY . /code/
WORKDIR /code/

# install python packages
RUN pip install konlpy JPype1
RUN apt-get -y install curl git
RUN apt-get update && \
    apt-get install -y automake libtool
RUN cd /code && \
    wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz && \
    tar -zxvf mecab-*-ko-*.tar.gz && \
    cd mecab-*-ko-* && \
    ./configure && \
    make && \
    make check && \
    make install && \
    ldconfig && \
    cd .. && \
    wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz && \
    tar xvzf mecab-ko-dic-2.1.1-20180720.tar.gz && \
    cd mecab-ko-dic-2.1.1-20180720 && \
    autoreconf && \
    ./configure && \
    make && \
    make install && \
    ln -sf /usr/local/bin/mecab-config /usr/bin/mecab-config && \
    git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git && \
    cd mecab-python-0.996/ && \
    python3 setup.py build && \
    python3 setup.py install


EXPOSE 8080

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port", "8080" ]