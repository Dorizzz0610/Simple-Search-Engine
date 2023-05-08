#!/bin/bash

cd ./web_interface
npm start &

cd ../backend
python main.py &