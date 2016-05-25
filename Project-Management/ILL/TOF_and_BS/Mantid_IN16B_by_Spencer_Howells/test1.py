# /opt/Mantid/etc/mantid.sh

from mantid.simpleapi import *
import numpy as np
import mantid.api as api

w1 = LoadILLIndirect( Filename='/net4/serdon/illdata/133/in16b/exp_9-13-477/rawdata/032854.nxs' )

# cd /net4/serdon/illdata/133/in16b/exp_9-13-477/rawdata/
# w1 = Load( Filename='032854:032861.nxs' )

