#! /bin/bash
export NODE=${NODE}
echo $NODE
echo $AC
echo $GEN
if [ "${GEN}" = "True" ];
  then
    komodod "${AC}" -gen -addnode="${NODE}"
  else
  	komodod "${AC}"  -addnode="${NODE}"
fi
