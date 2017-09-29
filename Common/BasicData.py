import pandas as pd
from WindPy import *
import time as tm
from Common import GlobalConfig


class Data():

    def __init__(self):
        # Initialize
        self.unit = 1e8
        self.config = GlobalConfig.GlobalConfig()

        # Get factor list
        FactorSheetExcel = self.config.getConfig('Excel', 'FactorSheet')
        self.FactorDF = pd.read_excel(FactorSheetExcel)
        self.FactorList = self.FactorDF["WindApiField"].values

        # Format date
        self.ThisYear = tm.strftime("%Y")
        self.EndDate = "%s-12-31" % str(int(self.ThisYear) - 1)
        self.StartDate = "2007-12-31"


