#!/bin/bash
echo "Once this script finishes, nltk downloader will open, click download to download the nltk corpus"
sleep 3
sudo apt-get install python3-pip
sudo pip3 install -U praw
sudo pip3 install -U nltk
sudo pip3 install -U numpy
sudo pip3 install -U matplotlib
sudo pip3 install -U wordcloud
sudo pip3 install -U tornado
python3 <<END
import nltk
nltk.download()
END