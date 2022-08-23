mkdir -p ~/.streamlit/

cd /tmp
sudo wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
sudo tar xvf mecab-0.996-ko-0.9.2.tar.gz

cd /tmp/mecab-0.996-ko-0.9.2
sudo ./configure
sudo make check
sudo make install

cd /tmp
wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
tar zxvf mecab-ko-dic-2.1.1-20180720.tar.gz

cd /tmp/mecab-ko-dic-2.1.1-20180720
sudo ./autogen.sh
sudo ./configure
sudo make
sudo make install

cd /tmp
git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
cd mecab-python-0.996
python3 setup.py build
python3 setup.py install

pip3 install mecab-python3

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

