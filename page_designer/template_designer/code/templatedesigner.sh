#!/bin/bash

CWD=`dirname $0`

cd $CWD

/usr/bin/env python $CWD/templatedesigner.py > $CWD/templatedesigner.log
