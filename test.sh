#!/bin/sh

expect -f login_git.sh
git reset --hard origin/derain_video
CUDA_VISIBLE_DEVICES=1 python manage.py test backend.test_rc.DerainTestCase.testDerainVideo
