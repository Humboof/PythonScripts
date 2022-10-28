import numpy as np
from scipy.interpolate import griddata


class SteamState:
    # two class variables - so we only have to read the tables once
    # in class methods, access the class variables as: class_name.class_variable
    #       in this case:  SteamState.shTable  and SteamState.satTable
    shTable = None  # superheated table data
    satTable = None  # saturated table data

    def __init__(self, pressure=None, T=None, x=None, v=None,
                 h=None, s=None, name=None):
        self.p = pressure  # pressure - kPa 
        self.T = T  # Temperature - degrees C 
        self.x = x  # quality (a value between 0 and 1) 
        self.v = v  # specific volume - m^3/kg 
        self.h = h  # enthalpy - kJ/kg 
        self.s = s  # entropy - kJ/(kg K) 
        self.name = name  # a useful identifier
        self.region = None  # 'superheated' or 'saturated'

        if SteamState.shTable is None:
            SteamState.shTable = np.loadtxt('superheated_water_table.txt', skiprows=1, unpack=True)

        if SteamState.satTable is None:
            SteamState.satTable = np.loadtxt('sat_water_table.txt', skiprows=1, unpack=True)


    def set(self, pressure=None, T=None, x=None, v=None, h=None, s=None, name=None):
        if pressure is not None: self.p = pressure
        if T is not None: self.T = T
        if x is not None: self.x = x
        if v is not None: self.v = v
        if h is not None: self.h = h
        if s is not None: self.s = s
        if name is not None: self.name = name


    def calcSuperheated(self):
        # we know we are not saturated, and THINK we might be superheated

        # get superheat table columns into nice names
        tcol, hcol, scol, pcol = SteamState.shTable

        # get state values into nice names so I don't have to type SELF so much
        pval=self.p; xval=self.x; hval=self.h; sval=self.s; vval=self.v; tval=self.T

        # we must know either temperature or pressure or both
        if pval is not None:  # pressure is known
            if tval is not None:  # p and T, so calculate h and s
                self.h = float(griddata((tcol, pcol), hcol, (tval, pval)))
                self.s = float(griddata((tcol, pcol), scol, (tval, pval)))
            elif hval is not None:  # p and h, so calculate T and s
                self.T = float(griddata((hcol, pcol), tcol, (hval, pval)))
                self.s = float(griddata((hcol, pcol), scol, (hval, pval)))
            elif sval is not None:  # p and s, so calculate h and T
                self.h = float(griddata((scol, pcol), hcol, (sval, pval)))
                self.T = float(griddata((scol, pcol), tcol, (sval, pval)))
            else:
                raise ValueError('Not enough properties specified in the superheated region')

        else:
            raise ValueError('Temperature or Pressure must be known')

        # we now are confident we are superheated!
        self.region = 'superheated'
        self.x = None
        self.v = None


    def calcSaturatedXP(self):
        # we know we are saturated, and we know PRESSURE and Quality
        # and that QUALITY is between 0 and 1
        psatbar = self.p / 100.0  # convert known pressure from kPa to bar
        xval = self.x

        # get the saturated table columns into nice names
        tscol, pscol, hfcol, hgcol, sfcol, sgcol, vfcol, vgcol = SteamState.satTable

        # Using the known pressure, interpolate on the saturation tables columns
        # at the known pressure
        sfval = float(griddata(pscol, sfcol, psatbar))
        sgval = float(griddata(pscol, sgcol, psatbar))
        vfval = float(griddata(pscol, vfcol, psatbar))
        vgval = float(griddata(pscol, vgcol, psatbar))
        hfval = float(griddata(pscol, hfcol, psatbar))
        hgval = float(griddata(pscol, hgcol, psatbar))
        tsat = float(griddata(pscol, tscol, psatbar))

        # Use the quality equation to get h, s and v
        self.h = hfval + xval * (hgval - hfval)
        self.s = sfval + xval * (sgval - sfval)
        self.v = vfval + xval * (vgval - vfval)

        self.T = float(tsat)
        self.region = 'saturated'


    def countProps(self):
        nProps = 0
        if self.p is not None: nProps += 1
        if self.T is not None: nProps += 1
        if self.h is not None: nProps += 1
        if self.s is not None: nProps += 1
        if self.v is not None: nProps += 1
        if self.x is not None: nProps += 1
        return nProps


    def calc(self):  # calculate and save the “missing” steam state properties attributes.

        # make sure 2 and only 2 properties are known to start the problem
        # I won't take off points if you skip this check
        if self.countProps() != 2:
            raise ValueError('Too many properties specified')

        # Will start by assuming we are saturated, so get nice column names for the saturated table
        tscol, pscol, hfcol, hgcol, sfcol, sgcol, vfcol, vgcol = SteamState.satTable

        # p or T must be known ... if not, then exit by raising an error
        if self.p is None and self. T is None:  # neither p nor T is known
            raise ValueError('Temperature or Pressure must be known')

        # Check for special case where both p and T are both known
        if self.p is not None and self.T is not None:
            # get saturation temperature for the given pressure
            psatbar = self.p / 100  # pressure in Bars for the Saturated Table
            tsat = float(griddata(pscol, tscol, psatbar))  # tsat for given pval
            if self.T > tsat or np.isnan(tsat):  # must be superheated
                self.calcSuperheated()
                return
            elif self.T < tsat:
                raise ValueError('Error - this function cannot operate in the sub-cooled region')
            else:
                raise ValueError('Not enough properties specified in the saturated region')

        # if we reach this location (haven't exited or raised an error) then either p or T is known but not both

        if self.p is not None:  # we know pressure but not temperature
            psatbar = self.p / 100  # pressure in Bars for the Saturated Table

        elif self.T is not None:  # or we know temperature but not pressure
            # assume saturated, age the saturation pressure for this Temperature
            psatbar = float(griddata(tscol, pscol, self.T))  # get saturation pressure in bars
            if np.isnan(psatbar):  # outside the saturated table so try superheated
                self.calcSuperheated()  # so must be superheated
                return


        def print(self):  # print the available (not None) State Attributes

            pass


def main():
    inlet = SteamState(p=8000, name='Turbine Inlet')
    inlet.set(x=0.5)  # 50 percent quality
    inlet.calc()
    inlet.print()

    reheat1 = SteamState(p=9000, h=4050, name='Reheat 1')
    reheat1.calc()
    reheat1.print()

    reheat2 = SteamState(p=8000, T=700)
    reheat2.calc()
    reheat2.print()

    outlet = SteamState(p=80, s=inlet.s, name='Turbine Exit')
    outlet.calc()
    outlet.print()

    another = SteamState(T=295, name='State 3')
    another.set(h=2100)
    another.calc()
    another.print()

    final = SteamState (T=295, name='State 4')
    final.set(h = 2100, s = 4.51)
    final.calc()
    final.print()