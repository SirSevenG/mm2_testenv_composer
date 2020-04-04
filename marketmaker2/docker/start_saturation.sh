#!/bin/bash

if [ ${SEED} = "True" ];
  then
  	source config_seed
  else
  	source config_saturation
fi

mm2 $config
