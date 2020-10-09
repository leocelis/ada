#!/usr/bin/env bash
# run with >source load.sh

echo '
      ___          _____          ___
     /  /\        /  /::\        /  /\
    /  /::\      /  /:/\:\      /  /::\
   /  /:/\:\    /  /:/  \:\    /  /:/\:\
  /  /:/~/::\  /__/:/ \__\:|  /  /:/~/::\
 /__/:/ /:/\:\ \  \:\ /  /:/ /__/:/ /:/\:\
 \  \:\/:/__\/  \  \:\  /:/  \  \:\/:/__\/
  \  \::/        \  \:\/:/    \  \::/
   \  \:\         \  \::/      \  \:\
    \  \:\         \__\/        \  \:\
     \__\/                       \__\/

  Leo Celis (c) 2020 - GPLv3 - ada-tool.com
'
# load env vars
source .env

# activate virtual env
source venv/bin/activate
