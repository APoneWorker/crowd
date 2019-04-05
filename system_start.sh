#!/bin/bash
python3 origin_capture.py > origin.log & python3 system_init.py > system.log & tail -f -n 50 system.log