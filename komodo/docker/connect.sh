#! /bin/bash
export NODE=${NODE}
export HOME=/
if [ "${GEN}" = "True" ];
  then
    komodod -ac_name="${AC}" -gen -addnode="${NODE}" -ac_cc=2 -ac_supply=100000 -ac_blocktime=45 -rpcbind=0.0.0.0 -rpcallowip=172.0.0.0/8
  else
  	komodod -ac_name="${AC}"  -addnode="${NODE}" -ac_cc=2 -ac_supply=100000 -ac_blocktime=45 -rpcbind=0.0.0.0 -rpcallowip=172.0.0.0/8
fi
