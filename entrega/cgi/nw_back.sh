#!/bin/bash

/bin/perl /nw_back/nw_back.pl

/bin/ls | /bin/grep -P "^[^.]*$" | /bin/xargs -d"\n" rm -r

/bin/rclone -v sync /nw_back/ nchw_bck:nw_back