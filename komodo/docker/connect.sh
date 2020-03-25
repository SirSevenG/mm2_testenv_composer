#! /bin/bash
export NODE=${NODE}
if [ "${GEN}" = "True" ];
  then
    komodod "${AC}" -gen
  else
  	komodod "${AC}"
fi
