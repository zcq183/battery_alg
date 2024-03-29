import numpy as np
from scipy.optimize import curve_fit


class CellEcm:
    """
    Equivalent circuit model (ECM) developed from HPPC battery cell data.

    Parameters
    ----------
    data : HppcData
        Data from the HPPC battery cell test. This parameter must be a class
        object of `HppcData`.
    params : module
        Model parameters for the battery calculations.

    Attributes
    ----------
    current : vector
        Current from HPPC battery during test [A]
    time : vector
        Time vector for HPPC battery test data [s]
    voltage : vector
        Voltage from HPPC battery during test [V]
    idp : tuple
        Indices representing short pulse section in the HPPC battery cell
        data. Indices are given for each 10% SOC section.
    idd : tuple
        Indices representing long discharge section where constant discharge
        occurs in the HPPC battery cell data. Indices are given for each 10%
        SOC section.

    Methods
    -------
    soc()
        Determine state of charge from current profile.
    points(soc)
        Get open circuit voltage points from HPPC data.
    ocv(v_pts, z_pts, soc)
        Interpolate open circuit voltage from HPPC data points.
    curve_fit_coeff(func, ncoeff)
        Determine curve fit coefficients from HPPC data.
    rctau_ttc(coeff)
        Determine RC values for each 10% SOC section.
    vt(soc, ocv, rctau)
        Determine battery voltage from equivalent circuit model.
    """

    def __init__(self, data, params):
        """
        Initialize with HPPC battery cell data and model parameters.
        """
        self.current = data.current
        self.time = data.time
        self.voltage = data.voltage
        self.idp = data.get_indices_pulse()
        self.idd = data.get_indices_discharge()

        self.eta_chg = params.eta_chg
        self.eta_dis = params.eta_dis
        self.q_cell = params.q_cell

    @staticmethod
    def func_otc(t, a, b, alpha):
        """
        Exponential function for a one time constant model (OTC).
        """
        return a - b * np.exp(-alpha * t)

    @staticmethod
    def func_ttc(t, a, b, c, alpha, beta):
        """
        Exponential function for a two time constants model (TTC).
        """
        return a - b * np.exp(-alpha * t) - c * np.exp(-beta * t)

    @staticmethod
    def get_rtau(rctau, z):
        """
        Determine tau and resistor values for any SOC.
        """

        # determine index where z is close to soc parameters
        soc = np.arange(0.1, 1.0, 0.1)[::-1]
        idx = abs(soc - z).argmin()

        # return resistor and tau values at z
        tau1 = rctau[:, 0][idx]
        tau2 = rctau[:, 1][idx]
        r0 = rctau[:, 2][idx]
        r1 = rctau[:, 3][idx]
        r2 = rctau[:, 4][idx]
        return tau1, tau2, r0, r1, r2

    def soc(self):
        """
        State of charge (SOC) of a battery cell based on the method from
        Gregory Plett's book [#plett]. Fully charged is SOC=1 and fully
        discharged is SOC=0. SOC is also referred to as `z` in some texts.

        Parameters
        ----------
        eta_chg : float
            Coulombic efficiency for charge, typically <= 1.0 [-]
        eta_dis : float
            Coulombic efficiency for discharge, typically = 1.0 [-]
        q : float
            Total capacity of battery cell [Ah]

        Returns
        -------
        z : vector
            State of charge at every time step in data [-]

        Note
        ----
        Battery cell capacity `q` is converted in this function from Ah to As.

        References
        ----------
        .. [#plett] Plett, Gregory L. Battery Management Systems, Volume I: Battery
           Modeling. Vol. 2. Artech House, 2015.
        """
        current = self.current
        time = self.time

        q = self.q_cell * 3600
        dt = np.diff(time)

        nc = len(current)
        z = np.ones(nc)

        for k in range(1, nc):
            i = current[k]
            if i > 0:
                eta = self.eta_chg
            else:
                eta = self.eta_dis
            z[k] = z[k - 1] + ((eta * i * dt[k - 1]) / q)

        return z

    def ocv(self, soc, pts=False, vz_pts=None):
        """
        Linearly interpolate the open circuit voltage (OCV) from state of charge
        points and voltage points in the HPPC data. Points are at 10% intervals
        of SOC. Returned OCV vector is same length as battery data used to
        determine SOC.

        Parameters
        ----------
        soc : vector
            State of charge for every time step in data [s]
        pts : bool, optional
            Return points in the HPPC data that are related to open circuit
            voltage. Default value is`False`.

        Returns
        -------
        ocv : vector
            Open circuit voltage [V] for every time step in data. Vector is
            same length as SOC vector.
        i_pts : vector, optional
            Current [A] at 100% SOC to 0% SOC in 10% increments.
        t_pts : vector, optional
            Time [s] at 100% SOC to 0% SOC in 10% increments.
        v_pts : vector, optional
            Voltage [V] at 100% SOC to 0% SOC in 10% increments.
        z_pts : vector, optional
            State of charge [-] at 100% SOC to 0% SOC in 10% increments.
        """
        if pts is True:
            id0 = self.idp[0]
            v_pts = np.append(self.voltage[id0], self.voltage[-1])
            z_pts = np.append(soc[id0], soc[-1])
            i_pts = np.append(self.current[id0], self.current[-1])
            t_pts = np.append(self.time[id0], self.time[-1])
            ocv = np.interp(soc, z_pts[::-1], v_pts[::-1])
            return ocv, i_pts, t_pts, v_pts, z_pts
        elif vz_pts is not None:
            v_pts, z_pts = vz_pts
            ocv = np.interp(soc, z_pts[::-1], v_pts[::-1])
            return ocv
        else:
            id0 = self.idp[0]
            v_pts = np.append(self.voltage[id0], self.voltage[-1])
            z_pts = np.append(soc[id0], soc[-1])
            ocv = np.interp(soc, z_pts[::-1], v_pts[::-1])
            return ocv

    def curve_fit_coeff(self, func, ncoeff):
        """
        Determine curve fit coefficients for each 10% change in SOC from HPPC
        data. These coefficients are used to calculate the RC parameters.

        Parameters
        ----------
        func : function
            Exponential function defining the curve.
        ncoeff : int
            Number of coefficients in the exponential function.

        Returns
        -------
        coeff : array
            Coefficients at each 10% change in SOC.
        """
        _, _, id2, _, id4 = self.idd
        nrow = len(id2)
        coeff = np.zeros((nrow, ncoeff))

        for i in range(nrow):
            start = id2[i]
            end = id4[i]
            t_curve = self.time[start:end]
            v_curve = self.voltage[start:end]
            t_scale = t_curve - t_curve[0]
            if ncoeff == 3:
                guess = v_curve[-1], 0.01, 0.01
            elif ncoeff == 5:
                guess = v_curve[-1], 0.01, 0.01, 0.001, 0.01
            popt, pcov = curve_fit(func, t_scale, v_curve, p0=guess)
            coeff[i] = popt

        return coeff

    def rctau_ttc(self, coeff):
        """
        Determine tau, resistor, and capacitor values (RC parameters) for each
        10% change in SOC from HPPC data.

        Parameters
        ----------
        coeff : array
            Coefficients at each 10% change in SOC from HPPC data.

        Returns
        -------
        rctau : array
            RC parameters as determined from HPPC data. Each row is for a 10%
            change in SOC. For example, RC parameters for SOC 100-90% is
            rctau[0] = tau1, tau2, r0, r1, r2, c1, c2 where
            tau1 : float
                First time constant [s]
            tau2 : float
                Second time constant [s]
            r0 : float
                Series resistance [Ω]
            r1 : float
                Resistance in first RC branch [Ω]
            r2 : float
                Resistance in second RC branch [Ω]
            c1 : float
                Capacitance in first RC branch [F]
            c2 : float
                Capacitance in second RC branch [F]
        """
        id0, id1, id2, _, _, = self.idd
        nrow = len(id0)
        rctau = np.zeros((nrow, 7))

        for k in range(nrow):
            di = abs(self.current[id1[k]] - self.current[id0[k]])
            dt = self.time[id2[k]] - self.time[id0[k]]
            dv = abs(self.voltage[id1[k]] - self.voltage[id0[k]])

            _, b, c, alpha, beta = coeff[k]

            tau1 = 1 / alpha
            tau2 = 1 / beta
            r0 = dv / di
            r1 = b / ((1 - np.exp(-dt / tau1)) * di)
            r2 = c / ((1 - np.exp(-dt / tau2)) * di)
            c1 = tau1 / r1
            c2 = tau2 / r2

            rctau[k] = tau1, tau2, r0, r1, r2, c1, c2

        return rctau

    def vt(self, soc, ocv, rctau):
        """
        Determine voltage from equivalent circuit model.
        """
        dt = np.diff(self.time)     # length of each time step, dt is not constant
        nc = len(self.current)      # total number of time steps based on current
        v0 = np.zeros(nc)           # initialize v0 array
        v1 = np.zeros(nc)           # initialize v1 array
        v2 = np.zeros(nc)           # initialize v2 array

        for k in range(1, nc):
            i = self.current[k]

            # get parameters at state of charge
            tau1, tau2, r0, r1, r2 = self.get_rtau(rctau, soc[k])

            # voltage in r0 resistor
            v0[k] = r0 * i

            # voltage in c1 capacitor
            tm1 = v1[k - 1] * np.exp(-dt[k - 1] / tau1)
            tm2 = r1 * (1 - np.exp(-dt[k - 1] / tau1)) * i
            v1[k] = tm1 + tm2

            # voltage in c2 capacitor
            tm3 = v2[k - 1] * np.exp(-dt[k - 1] / tau2)
            tm4 = r2 * (1 - np.exp(-dt[k - 1] / tau2)) * i
            v2[k] = tm3 + tm4

        vt = ocv + v0 + v1 + v2
        return vt
