#!/bin/bash

if [ ${SEED} = "True" ];
  then
  	source config_seed
  else
  	source config_saturation
fi

marketmaker-mainnet $config
