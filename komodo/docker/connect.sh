#! /bin/bash
if [ "${GEN}" = "True" ];
  then
    komodod -ac_name="${AC}" -gen -addnode="${NODE}" -ac_cc=2 -ac_supply=100000 -ac_blocktime=45 -rpcbind=0.0.0.0 -rpcallowip=0.0.0.0/0
  else
  	komodod -ac_name="${AC}"  -addnode="${NODE}" -ac_cc=2 -ac_supply=100000 -ac_blocktime=45 -rpcbind=0.0.0.0 -rpcallowip=0.0.0.0/0
fi
