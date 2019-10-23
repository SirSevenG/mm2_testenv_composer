#! /bin/bash
if [ ${GEN} = "True" ];
  then
    ./komodod -ac_name=${CHAIN} -ac_cc=${CC} -ac_supply=${SUPPLY} --addnode=${NODE} -gen -server -rest -rpcbind=0.0.0.0  -rpcbind=[::] -rpcallowip=172.0.0.0/8
  else
  	./komodod -ac_name=${CHAIN} -ac_cc=${CC} -ac_supply=${SUPPLY} --addnode=${NODE} -server -rest -rpcbind=0.0.0.0 -rpcbind=[::] -rpcallowip=172.0.0.0/8
fi
