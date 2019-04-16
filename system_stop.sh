#!/bin/bash
kill -9 $(ps -e|grep "origin_capture" |awk \'{print $1}\')
kill -9 $(ps -e|grep "system_init" |awk \'{print $1}\')