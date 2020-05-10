#!/bin/bash

if [ ${SEED} = "True" ];
  then 
  	source config_seed
  else
  	source config_client
fi

marketmaker-mainnet $config
