#! /bin/bash
export NODE=${NODE}
echo $NODE
echo $AC
echo $GEN
if [ "${GEN}" = "True" ];
  then
    komodod "${AC}" -gen -addnode="${NODE}" -ac_name=WSG -ac_cc=2 -ac_supply=100000 -ac_blocktime=45 -rpcbind=0.0.0.0 -rpcallowip=172.0.0.0/8
  else
  	komodod "${AC}"  -addnode="${NODE}" -ac_name=WSG -ac_cc=2 -ac_supply=100000 -ac_blocktime=45 -rpcbind=0.0.0.0 -rpcallowip=172.0.0.0/8
fi
