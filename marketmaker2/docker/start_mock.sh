#!/bin/bash

if [ ${SEED} = "True" ];
  then
  	source config_seed
  else
  	source config_saturation
fi

nohup mm2 $config &>/dev/null &
python3 emulate.py
