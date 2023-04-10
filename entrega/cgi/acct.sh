#!/bin/bash

sa -nac | head -15 | tail +2 > commands.txt

/usr/bin/perl /root/acct/acct.pl

