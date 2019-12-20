#!/usr/bin/bash -x

export ORACLE_HOME=/usr/lib/oracle/12.2/client64
export LD_LIBRARY_PATH=/usr/lib/oracle/12.2/client64/lib
export PATH=$PATH:/usr/lib/oracle/12.2/client64/bin

cd /home/eric/projects/ERICSSON

python3 collect_ericsson_mss_mgmap.py