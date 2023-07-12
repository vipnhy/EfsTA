import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.ticker as mticker
import os
import numpy as np
from lmfit import minimize, Parameters, fit_report
import scipy.integrate as scint
from models import Models
import pandas as pd
mpl.use("QtAgg")
plt.style.use('./AK_Richert.mplstyle')
#plt.style.use('default')
plt.ion()

class Model:

    # Initiation Of The Class

    def __init__(self,csv_filename, d_limits, l_limits, model, opt_method, ivp_method): 
        #         delays_filename, spectra_filename, lambdas_filename,
        #         d_limits, l_limits, model, opt_method, ivp_method):
        """
        Initiates an object of the class Model with preset data and model.
        Presets a list of colors for the 3-in-1 plot.

        Parameters
        ----------
        delays_filename : string
            The path to the file for the delay values.
        spectra_filename : string
            The path to the file for the spectra values.
        lambdas_filename : string
            The path to the file for the lambda values.
        d_limits : list with two int/float elements
            Lower and upper limits for the delay values.
        l_limits : list with two int/float elements
            Lower and upper limits for the lambda values.
        model : int/string
            Variable for the choice of model (DAS or which SAS).

        Returns
        -------
        None.

        """
        #self.d_borders = self.findBorders(d_limits, delays_filename)
        #self.l_borders = self.findBorders(l_limits, lambdas_filename)
        #self.name = self.findName(delays_filename)
        #self.delays = self.initDelays(delays_filename)
        #self.spectra = self.initSpectra(spectra_filename)
        #self.lambdas = self.initLambdas(lambdas_filename)
        self.d_borders = self.findBordersbyCSV(d_limits, csv_filename, type="delay")
        self.l_borders = self.findBordersbyCSV(l_limits, csv_filename, type="lambda")
        self.name = "test"
        self.delays, self.lambdas, self.spectra = self.initDatabyCSV(csv_filename, self.d_borders, self.l_borders)
        self.model = model
        self.opt_method = opt_method
        self.ivp_method = ivp_method

    def initDatabyCSV(self, csv_file_name,d_limits,l_limits):
        df = self.readCSV(csv_file_name)
        df = df.iloc[l_limits[0]:l_limits[1],d_limits[0]:d_limits[1]]
        delays = df.columns.values
        lambdas = df.index.values
        spectra = df.values
        return delays, lambdas, spectra

    def readCSV(self, csv_file_name):
        df = pd.read_csv(csv_file_name, index_col=0)
        df = df.iloc[:-11,:]
        df.columns = df.columns.str.replace("0.000000.1","0")
        df.index = pd.to_numeric(df.index)
        df.columns = pd.to_numeric(df.columns)
        #去除nan
        df = df.fillna(0)
        #设置inf为最大值
        df = df.replace(np.inf, 0)
        #设置-inf为最小值
        df = df.replace(-np.inf, 0)
        return df


    def findBordersbyCSV(self, limits, csv_filename, type="delay"):
        """
        Finds the indices for the chosen limits in a set of values.
        If none are chosen, the borders will automatically be set.

        Parameters
        ----------
        limits : list with two int/float elements
            Lower and upper limits for the values in the given file.
        filename : string
            The path to the file for the values.

        Returns
        -------
        borders : list with two int elements
            Indexes for the lower and upper limit of the values in the file.

        """
        df = self.readCSV(csv_filename)
        if type == "delay":
            values = df.columns.values
        elif type == "lambda":
            values = df.index.values
        borders = [0, 1]
        if limits == None:
            limits = [None, None]
        if limits[0] == None:
            limits[0] = min(values)
        if limits[1] == None:
            limits[1] = max(values)
            
        borders[0] = np.absolute(values-limits[0]).argmin()
        borders[1] = np.absolute(values-limits[1]).argmin()

        return borders
    

    def findBorders(self, limits, filename):
        """
        Finds the indices for the chosen limits in a set of values.
        If none are chosen, the borders will automatically be set.

        Parameters
        ----------
        limits : list with two int/float elements
            Lower and upper limits for the values in the given file.
        filename : string
            The path to the file for the values.

        Returns
        -------
        borders : list with two int elements
            Indexes for the lower and upper limit of the values in the file.

        """
        values = np.genfromtxt(filename)
        borders = [0, 1]
        if limits == None:
            limits = [None, None]
        if limits[0] == None:
            limits[0] = min(values)
        if limits[1] == None:
            limits[1] = max(values)
        borders[0] = round(np.absolute(values-limits[0]).argmin(),2)
        borders[1] = round(np.absolute(values-limits[1]).argmin(),2)
        return borders

    def findName(self, delays_filename):
        """
        Find the name of the mesured data.

        Parameters
        ----------
        delays_filename : string
            The path to the file for the delay values.

        Returns
        -------
        name : string
            Name of the mesured data.

        """
        temp = delays_filename[::-1]
        temp = temp.index("/")
        name = delays_filename[-temp:-11]
        path = delays_filename[:-temp]
        if not os.path.exists(path+'analysis'):
            os.makedirs(path+'analysis')
        self.path = delays_filename[:-temp]+"analysis/"
        return name

    def initDelays(self, delays_filename):
        """
        Applys the border to the original data of the delays.

        Parameters
        ----------
        delays_filename : string
            The path to the file for the delay values.

        Returns
        -------
        delays : np.array
            Contains the values of the delays within the chosen borders.

        """
        values = np.genfromtxt(delays_filename)
        delays = values[self.d_borders[0]: self.d_borders[1]]
        return delays

    def initLambdas(self, lambdas_filename):
        """
        Applys the border to the original data of the lambdas.

        Parameters
        ----------
        lambdas_filename : string
            The path to the file for the lambda values.

        Returns
        -------
        lambdas : np.array
            Contains the values of the lambdas within the chosen borders.

        """
        values = np.genfromtxt(lambdas_filename)
        lambdas = values[self.l_borders[0]: self.l_borders[1]]
        return lambdas

    def initSpectra(self, spectra_filename):
        """
        Applys the border to the original data of the spectra.

        Parameters
        ----------
        spectra_filename : string
            The path to the file for the spectra values.

        Returns
        -------
        spectra : np.array
            Contains the values of the spectra within the chosen borders.

        """
        values = np.genfromtxt(spectra_filename)
        spectra = values[self.l_borders[0]: self.l_borders[1],
                         self.d_borders[0]: self.d_borders[1]]
        return spectra

    # Decay Associated Spectra

    def genE_tau(self, tau):
        """
        Generatest the matrix E with different values for the delays in every
        column and different values for tau in the rows.

        Parameters
        ----------
        tau : list
            A list of the given values for tau, the decay constant.

        delays : np.array
              The measured delays of the TA-spectrum.

        Returns
        -------
        E_tau : np.array
            The matrix of E_tau with the exponential decay functions.

        """
        E_tau = np.zeros(shape=(len(tau), len(self.delays)))
        for i in range(len(tau)):
            for j in range(len(self.delays)):
                E_tau[i][j] = -self.delays[j] / tau[i]
        E_tau = np.exp(E_tau)
        return E_tau

    # Species Associated Spectra

    def setInitialConcentrations(self, C_0):
        """
        Creates an array with the initial concentrations for the GTA.

        Parameters
        ----------
        C_0 : list
            The list that contains values for C_0 set by the user.
            Can be empty.

        Returns
        -------
        C_0 : np.array/list
            Contains either the user-input for C_0 or a concentration of 1 for
            the first species and 0 for all the others.

        """
        if C_0 == []:
            C_0 = np.zeros(self.n)
            C_0[0] = 1
        self.C_0 = C_0
        return C_0

    def calcdCdt(self, delays, C_0):
        """
        Calculates the matrix for the derivate of the concentration
        by the time.

        Parameters
        ----------
        delays : np.array
              The measured delays of the TA-spectrum.
        C_0 : np.array/list
            contains either the user-input for C_0 or a concentration of 1 for
            the first species and 0 for all the others

        Returns
        -------
        dCdt : np.array
            derivate of the concentration by the time

        """
        dCdt = self.K @ C_0
        return dCdt

    def solveDiff(self, K, ivp_method):
        """
        Solves the differential equation of dCdt = K·C.

        Parameters
        ----------
        K : np.array
            The matrix with the reaction constants for each concentration.
        ivp_method: string
            The algorithm used by the initial value problem solver.

        Returns
        -------
        C_t : np.array
            Contains the concentration of each species at each point of
            time in delays.

        """
        self.K = K
        Z = scint.solve_ivp(self.calcdCdt, [min(self.delays), max(self.delays)],
            self.C_0, t_eval=self.delays, method=ivp_method)
        C_t = Z.get("y")
        return C_t

    def getK(self, tau):
        """
        Outputs the matrix K for given reaction constants x.

        Parameters
        ----------
        tau : list, np.array
            An array of the reaction rate constants for the SAS.

        Returns
        -------
        K : np.array
            A 2D array which corresponds to the reaction rate constant matrix
            with n-species.
        n : int
            The number of species.

        """
        if (self.model == "custom model" or self.model == "custom matrix"):
            Tau = self.regenM(tau)
            n = Tau.shape[0]
            ones = np.full(Tau.shape, 1)
            K = np.divide(ones, Tau, out=np.zeros_like(Tau),
                                where=Tau!=0)
        else:
            ones = np.full(np.array(tau).shape, 1)
            k = np.divide(ones, tau, out=np.zeros_like(tau, dtype='float64'),
                          where=tau!=0)
            mod = Models(k)
            K, n = mod.getK(self.model)
        self.n = n
        self.K = K
        return K, n
    
    def getM_lin(self, tau_guess):
        """
        Transforms the custom matrix for the SAS in a linear list and a matrix
        with 1 as placeholders for the corresponding values.
        Saves the matrix M_ones as an attribute.

        Parameters
        ----------
        tau_guess : list, np.array
            The custom matrix for the SAS with the decay constants tau.

        Returns
        -------
        tau : np.array
            An array with the decay constants tau of the custom matrix.

        """
        ones = np.full(tau_guess.shape, 1)
        k_guess = np.divide(ones, tau_guess, out=np.zeros_like(tau_guess),
                            where=tau_guess!=0)
        M_lin = []
        M_ones = np.zeros(k_guess.shape)
        for i in range(k_guess.shape[0]):
            for j in range(k_guess.shape[1]):
                if i == j and i != k_guess.shape[0]-1:
                    k_guess[i][j] = 0
                if k_guess[i][j] != 0:
                    M_ones[i][j] = 1
                    M_lin.append(abs(k_guess[i][j]))
        tau = 1/np.array(M_lin)
        self.M_ones = M_ones
        return tau
        
    def regenM(self, tau_guess):
        """
        Regenerates the custom matrix with the fitted values found in x_guess.
        Replaces the 1 in the M_ones matrix with the corresponding values.

        Parameters
        ----------
        tau_guess : list, np.array
            The fitted decay constants for the SAS.

        Returns
        -------
        M : np.array
            The custom matrix for the SAS with the decay constants tau.

        """
        a = 0
        M = np.zeros(self.M_ones.shape)
        for i in range(self.M_ones.shape[0]):
            for j in range(self.M_ones.shape[1]):
                if self.M_ones[i][j] == 1:
                    M[i][j] = tau_guess[a]
                    if j != self.M_ones.shape[0]-1:
                        M[j][j] -= tau_guess[a]
                    a += 1
        M[-1][-1] *= -1
        return M
    
    def setTauBounds(self, tau_low, tau_high, tau):
        """
        Responsible for the setting of the bounds to be used in the optimizing
        of the tau values.

        Parameters
        ----------
        tau_low : list
            A list which contains the lower bounds for the respective tau
            values.
        tau_high : list
            A list which contains the upper bounds for the respective tau
            values.
        tau : list, np.array
            An array containing the decay constants tau.

        Returns
        -------
        None.

        """
        if tau_low == []:
            tau_low = [None for i in tau]
        if tau_high == []:
            tau_high = [None for i in tau]
        for i in range(len(tau_low)):
            if tau_low[i] == 0 or tau_low[i] == None:
                tau_low[i] = 0.01
        self.tau_low = tau_low
        self.tau_high = tau_high

    def getTauBounds(self, tau):
        """
        This method outputs the bounds of the tau values for their optimizing.

        Parameters
        ----------
        tau : list, np.array
            An array containing the decay constants tau.

        Returns
        -------
        bounds : list
            A list of the bounds for each tau value.

        """
        if self.model == 0:
            bounds = [(0.01, None) for i in tau]
        else:
            bounds = list(zip(self.tau_low, self.tau_high))
        return bounds

    def getM(self, tau):    
       """
       Outputs the matrix which will be used in the matrix reconstruction
       algorithm to obtain the fitted spectra A_fit. For the DAS it is the
       matrix E_tau and for SAS it is the matrix C_t from the solved
       differential equation.

       Parameters
       ----------
       tau : list, np.array
           An array containing the decay constants tau.

       Returns
       -------
       M : np.array
           The matrix for the matrix reconstruction algorithm.

       """
       if self.model == 0:  # GLA
           M = self.genE_tau(tau)
           self.n = len(tau)
       else:  # GTA
           self.K, n = self.getK(tau)
           M = self.solveDiff(self.K, self.ivp_method)
       return M

    def calcD_tau(self, tau):
        """
        Calculates the matrix D_tau.

        Parameters
        ----------
        tau : list, np.array
            An array containing the decay constants tau.

        Returns
        -------
        D_tau : np.array
            The matrix D_tau.

        """
        
        res1 = self.spectra @ self.M.T
        res2 = self.M @ self.M.T
        inv = np.linalg.inv(res2)
        D_tau = res1 @ inv
        return D_tau

    def calcA_tau(self, tau):
        """
        Generates the reconstructed spectra matrix for the values of tau.

        Parameters
        ----------
        tau : list, np.array
            An array containing the decay constants tau.

        Returns
        -------
        A_tau : np.array
            The reconstructed data matrix for the values of tau.

        """
        D_tau = self.calcD_tau(tau)
        A_tau = D_tau @ self.M
        return A_tau

    def getDifference(self, tau):
        """
        Calculates the measure of difference between the initial spectra
        matrix and the calculated A_tau matrix with given values for tau_guess
        and self.tau_fix, if DAS.

        Parameters
        ----------
        tau_guess : list, np.array
            A list of the variables tau_guess for the DAS or all tau values for
            the SAS.

        Returns
        -------
        getDifferences : np.ndarray
            Difference between the modeled data and the experimental data.

        """
        tau_sum = list(tau.valuesdict().values())
        self.M = self.getM(tau_sum)
        difference = self.calcA_tau(tau_sum) - self.spectra
        return difference
    
    def findTau_fit(self, preparam, opt_method):
        """
        The function takes the variable tau_guess and optimizes their values,
        so that ChiSquare takes a minimal value. It outputs a list of the 
        optimized tau values and the non-varied ones, if GLA was used.

        Parameters
        ----------
        tau_fix : list, np.array
            A list of the variables tau_fix for the DAS. Empty for SAS.
        tau_guess : list, np.array
            A list of the variables tau_guess for the DAS or all tau values for
            the SAS.
        opt_method: string
            The algorithm used by the optimization function.

        Returns
        -------
        tau_sum : list
            The fitted parameters tau_fit and the fixed values tau_fix combined.

        """


        params = Parameters()
        self.tau_fit = []
        bounds = self.getTauBounds(preparam)
        #for i in range(len(preparam)):
        #     params.add('tau'+str(i), preparam[i][0],
        #                    min=bounds[i][0], max=bounds[i][1],vary=preparam[i][1])
        params.add('tau0', preparam[1][0],min=bounds[0][0], max=bounds[0][1],vary=preparam[1][1])
        res_fit = minimize(self.getDifference, params, method=opt_method)
        fit_rep = fit_report(res_fit)
        if hasattr(res_fit, "success"):
            if res_fit.success is False:
                print("Fitting unsuccesful!")
        for name, param in res_fit.params.items():
            self.tau_fit.append(param.value)
        if (self.model == "custom model" or self.model == "custom matrix"):
            tau_sum = self.regenM(self.tau_fit)
        else:
            tau_sum = self.tau_fit
        return tau_sum, fit_rep

    def calcD_fit(self):
        """
        Calculates D_fit from the previously calculated self.tau_fit and x_fix,
        if DAS.

        Returns
        -------
        D_fit : np.array
            Matrix D with the fitted values for tau.

        """
        self.M_fit = self.getM(self.tau_fit)
        res1 = self.spectra @ self.M_fit.T
        bra1 = np.linalg.inv(self.M_fit @ self.M_fit.T)
        D_fit = res1 @ bra1
        self.D_fit = D_fit
        return D_fit

    def calcA_fit(self):
        """
        Generates the reconstructed spectra matrix with the matrices
        self.D_fit and self.M_fit.

        Returns
        -------
        A_fit : np.array
            The reconstructed data matrix for the values of tau_fit and x_fix,
            if DAS.

        """
        A_fit = self.D_fit @ self.M_fit
        self.spec = A_fit
        return A_fit

    def calcResiduals(self):
        """
        Calculates the difference between the original spectra and the
        calculated spectra to obtain residuals.

        Returns
        -------
        residuals : np.array
            Difference between spectra (original data) and spec (fitted data).

        """
        mul1 = self.D_fit @ self.M_fit
        self.residuals = mul1 - self.spectra
        return self.residuals

    # Plotting of the data

    def setv_min(self, data, mul):
        """
        For the given data and multiplicity, this function will determine the
        minimal value for the colorbar.

        Parameters
        ----------
        data : np.array
            An array containing data.
        mul : float
            The value by which data will be multiplied.

        Returns
        -------
        v_min : float
            The minimal value for the colorbar.

        """
        flat_A = data.flatten()
        v_min = min(flat_A) * mul
        return v_min

    def setv_max(self, data, mul):
        """
        For the given data and multiplicity, this function will determine the
        maximal value for the colorbar.

        Parameters
        ----------
        data : np.array
            An array containing data.
        mul : float
            The value by which data will be multiplied.

        Returns
        -------
        v_max : float
            The maximal value for the colorbar.

        """
        flat_A = data.flatten()
        v_max = max(flat_A) * mul
        return v_max

    def findNearestIndex(self, x, data):
        """
        Finds the nearest indices for the elements in x in the data.

        Parameters
        ----------
        x : list
            A list of values which are within the borders of the data.
        data : np.array
            An array containing data.


        Returns
        -------
        x : list
            The nearest indices for the given values.

        """
        x = list(x)
        for i in range(len(x)):
            mini = np.argmin(abs(data - x[i]))
            x[i] = mini
        return x
    
    def log_tick_formatter(self, val, pos=None):
        '''
        A logarithmic tick formatter for the 3D contour plot.

        Parameters
        ----------
        val : float
            The value to be put into log scaling.

        Returns
        -------
        string
            The formated axis tick.

        '''
        return r"$10^{{{:.0f}}}$".format(val)
    
    def plot1(self, grid, wave, wave_index, spectra, mul, labels):
        """
        Plots a subplot of delays against absorption change for chosen
        wavelenghts.

        Parameters
        ----------
        grid : plt.GridSpec
            The object of the grid for all subplots.
        wave : list
            Wavelenghts which should be plotted.
        wave_index : list
            Indexes for the wavelengths to be plotted .
        spectra : np.array
            Contains the values of the spectra.

        Returns
        -------
        None.

        """
        ltx = str(mul).count("0")
        unit = ""
        if "/" in labels[0]:
            unit = labels[0].split("/")[1]
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        
        ax1 = plt.subplot(grid[0, 0])
        ax1.set_yscale("log")
        ax1.set_xlabel(labels[2] + dot)
        ax1.set_ylabel(labels[1])

        for i, ind in enumerate(wave_index):
            ax1.plot(
                spectra[ind],
                self.delays,
                label=str(wave[i]) + unit
            )
        ax1.axvline(0, color="black",lw = 0.5 , alpha=0.75)
        temp = np.concatenate([spectra[i]
                              for i in wave_index])
        ax1.axis(
            [
                1.05 * min(np.array(temp)),
                1.05 * max(np.array(temp)),
                min(self.delays),
                max(self.delays),
            ]
        )
        ax1.set_xticks(())
        ax1.tick_params(bottom=False)
        ax1.legend(loc="upper left", frameon=False, labelcolor="linecolor",
                   handlelength=0,fontsize=11)

    def plot2(self, grid, wave, time, v_min, v_max, spectra, add, cont, mul, labels):
        """
        Plots a subplot with a heatmap of the absorption change in delays
        against lambdas.

        Parameters
        ----------
        grid : plt.GridSpec
            The object of the grid for all subplots.
        wave : list
            Wavelenghts which should be plotted.
        time : list
            Delays which should be plotted.
        v_min : float
            Lower limit for the colorbar.
        v_max : float
            Lower limit for the colorbar.
        spectra : np.array
            Contains the values of the spectra.
        add : string
            Addition to the title of the subplot.
        cont : float
            Determines how much contour lines will be shown in the 2D plot.
            High values will show more lines.

        Returns
        -------
        ax2 : plt.subplot
            The axis of this subplot.
        cb : plt.colorbar
            The object colorbar.

        """
        ax2 = plt.subplot(grid[0, 1])
        ax2.set_yscale("log")
        ax2.set_xlabel(labels[0])
        A_t = spectra.T
        pcm = ax2.pcolormesh(
            self.lambdas,
            self.delays,
            A_t,
            cmap=plt.cm.seismic,
            norm=col.TwoSlopeNorm(vcenter=0, vmin=v_min, vmax=v_max),
            shading="auto",
        )
        if v_min is None:
            v_min = self.setv_min(spectra, mul)
        if v_max is None:
            v_max = self.setv_max(spectra, mul)
        cb = plt.colorbar(pcm)
        cb.set_ticks([v_min, 0, v_max])
        contours = ax2.contour(
            self.lambdas,
            self.delays,
            A_t,
            levels=np.arange(v_min, v_max, (1 / cont) * (v_max - v_min)),
            colors="black",
            linewidths=0.7,
            linestyles="solid",
        )
        ax2.clabel(contours, inline=False, fontsize=0)

        for i in wave:
            ax2.axvline(i,color="black", linestyle="-.")

        for i in time:
            ax2.axhline(i, color="black", linestyle="dotted")

        ax2.axis(
            [
                min(self.lambdas),
                max(self.lambdas),
                [min(self.delays) if min(self.delays) > 0 else 10 ** (-2)][0],
                max(self.delays),
            ]
        )
        ax2.set_yticks(())
        
        return ax2, cb

    def plot3(self, grid, time, time_index, spectra, mul, labels):
        """
        Plots a subplot of absorption change against wavelenghts for chosen
        delays.

        Parameters
        ----------
        grid : plt.GridSpec
            The object of the grid for all subplots.
        time : list
            Delays which should be plotted.
        time_index : list
            Indexes for the delays to be plotted.
        spectra : np.array
            Contains the values of the spectra.

        Returns
        -------
        None.

        """
        ltx = str(mul).count("0")
        unit = ""
        if "/" in labels[1]:
            unit = labels[1].split("/")[1]
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        ax3 = plt.subplot(grid[0, 2])
        ax3.set_ylabel(labels[2] + dot)
        ax3.set_xlabel(labels[0])
        y = np.zeros(len(self.lambdas))
        hoehe = 0
        temp = np.zeros(len(self.lambdas))
        for i, ind in enumerate(time_index):
            for j in range(len(self.lambdas)):
                temp[j] = spectra[j][ind]
                y[j] = temp[j] + hoehe
            if ind == time_index[0]:
                mini = min(y)
            ax3.plot(self.lambdas, y, color="black")
            ax3.annotate(
                str(time[i]) + unit, (0.5 * (min(self.lambdas) +
                                 max(self.lambdas)), hoehe)
            )
            ax3.axhline(hoehe, color="black", lw = 0.5, alpha = 0.75)
            hoehe += 1.1 * (abs(max(temp)) + abs(min(temp)))
        ax3.axis([min(self.lambdas), max(self.lambdas), 1.1 * mini,
                  1.1 * max(y)])
        ax3.set_yticks(())
        
    def plot3D(self, spectra,v_min, v_max, mul, labels, add=""):
        """
        Allows for the creation of a 3D contour plot. Just because I can.        

        Parameters
        ----------
        spectra : np.array
            Contains the values of the spectra.
        v_min : float
            Lower limit for the colorbar.
        v_max : float
            Upper limit for the colorbar.
        cont : float
            Determines how much contour lines will be shown in the 2D plot.
            High values will show more lines.
        add : string, optional
            Addition to the title of the subplot. The default is "".
        mul : float
            The value by which the spectra will be multiplied.
            The default is 1.

        Returns
        -------
        None.

        """
        fig, ax = plt.subplots(figsize=(11.2,8),subplot_kw={"projection" : "3d"})
        log_delay = np.log10(abs(self.delays))
        ltx = str(mul).count("0")
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        if v_min is None:
            v_min = self.setv_min(spectra, mul)
        if v_max is None:
            v_max = self.setv_max(spectra, mul)
        X, Y = np.meshgrid(self.lambdas, log_delay)
        Z = spectra.T*mul
        ax = plt.axes(projection='3d')
        ax.contour3D(X,Y,Z,80,cmap='seismic')
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[0] + dot)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(self.log_tick_formatter))
        yticks = np.linspace(min(log_delay), max(log_delay), 4)
        yticks[0] = -1
        ax.set_yticks(yticks)
        ax.view_init(20,250)
        plt.savefig(self.path + self.name + "3DContour" + ".png")
        
    def plotCustom(self, spectra, wave, time, v_min, v_max, custom, cont, mul, labels,
                   add=""):
        """
        Allows for the creation of 1-3 subplots in one plot.

        Parameters
        ----------
        spectra : np.array
            Contains the values of the spectra.
        wave : list
            Wavelenghts which should be plotted.
        time : list
            Delays which should be plotted.
        v_min : float
            Lower limit for the colorbar.
        v_max : float
            Upper limit for the colorbar.
        custom : string
            Describes which subplots will be plotted.
        cont : float
            Determines how much contour lines will be shown in the 2D plot.
            High values will show more lines.
        mul : float
            The value by which the spectra will be multiplied.
            The default is 1.
        add : string, optional
            Addition to the title of the subplot. The default is "".

        Returns
        -------
        None.

        """
        ltx = str(mul).count("0")
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        if v_min is None:
            v_min = self.setv_min(spectra, mul)
        if v_max is None:
            v_max = self.setv_max(spectra, mul)
        wave_index = self.findNearestIndex(wave, self.lambdas)
        time_index = self.findNearestIndex(time, self.delays)
        space = 0

        if custom == "1":
            width = 2.5
            w1 = 1.0
            w2 = 0
            w3 = 0
        elif custom == "2":
            width = 5.2
            w1 = 0
            w2 = 4.7
            w3 = 0
        elif custom == "3":
            width = 2
            w1 = 0
            w2 = 0
            w3 = 1.5
        elif custom == "1+2":
            width = 7
            w1 = 1.0
            w2 = 3.7
            w3 = 0
        elif custom == "1+3":
            width = 5
            w1 = 1.0
            w2 = 0
            w3 = 1.5
            space = 0.25
        elif custom == "2+3":
            width = 7
            w1 = 0
            w2 = 4.7
            w3 = 1.5
        elif custom == "1+2+3":
            width = 9
            w1 = 1.0
            w2 = 3.7
            w3 = 1.5

        fig = plt.figure(
            figsize=(width, 3), constrained_layout=False, frameon=True
        )
        grid = plt.GridSpec(1, 3, wspace=space, width_ratios=[w1, w2, w3])

        if w1 != 0:
            self.plot1(grid, wave, wave_index, spectra*mul, mul, labels)
        if w2 != 0:
            ax2, cb = self.plot2(grid, wave, time, v_min,
                                 v_max, spectra*mul, add, cont, mul, labels)
            if w3 == 0:
                cb.set_label(labels[2] + dot)
            if w2 == 4.7:
                ax2.yaxis.set_major_locator(mticker.LogLocator())
                ax2.set_ylabel(labels[1])
        if w3 != 0:
            self.plot3(grid, time, time_index, spectra*mul, mul, labels)
        grid.tight_layout(fig)
        plt.savefig(self.path + self.name + add  + ".png",
            bbox_inches="tight")

    def plotSolo(self, spectra, wave, time, v_min, v_max, solo, cont, mul, labels, add=""):
        """
        Allows for the plotting of improved single plots.

        Parameters
        ----------
        spectra : np.array
            Contains the values of the spectra.
        wave : list
            Wavelenghts which should be plotted.
        time : list
            Delays which should be plotted.
        v_min : float
            Lower limit for the colorbar.
        v_max : float
            Upper limit for the colorbar.
        solo : string
            Describes which subplots will be plotted.
        cont : float
            Determines how much contour lines will be shown in the 2D plot.
            High values will show more lines.
        mul : float
            The value by which the spectra will be multiplied.
            The default is 1.
        add : string, optional
            Addition to the title of the subplot. The default is "".
            
        Returns
        -------
        None.

        """
        if solo == "WS":
            self.plotWSlices(wave, spectra, mul, labels, add)
        if solo == "DS":
            self.plotDSlices(time, spectra, mul, labels, add)
        if solo == "H":
            self.plotHeat(wave, time, v_min, v_max, spectra, cont, mul, labels, add)
            
    def plotData(self, x, y, x_label, y_label, label, add=""):
        """
        Allows for the plotting of any 2D data.

        Parameters
        ----------
        x : np.array
            values for the x-axis
        y : np.array
            values for the x-axis
        x_label : string
            label for the x-axis
        y_label : string
            label for the y-axis
        add : string, optional
            Addition to the title of the plot. The default is "".
        label : string, optional
            label for the graphs in the plot

        Returns
        -------
        None.

        """
        fig, ax = plt.subplots()
        temp = y.flatten()
        ax.axis(
            [
                min(x),
                max(x),
                1.1 * min(temp),
                1.1 * max(temp)
            ]
        )
        ax.plot(x, y)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if add == "_GTA_kin" or add == "_GLA_kin":
            ax.set_xscale("log")
            fig.set_size_inches(7.6,4)
        else:
            ax.axhline(0, color="black", lw=0.5, alpha = 0.75)
        if label != None:
            ax.legend(label, frameon=False, labelcolor="linecolor",
                       handlelength=0, loc="lower right")
        plt.savefig(self.path + self.name + add  + ".png",
                    bbox_inches="tight")
        
        
    def plotWSlices(self, wave, spectra, mul, labels, add):
        """
        Plots a subplot of delays against absorption change for chosen
        wavelenghts.

        Parameters
        ----------
        wave : list
            Wavelenghts which should be plotted.
        wave_index : list
            Indexes for the wavelengths to be plotted .
        spectra : np.array
            Contains the values of the spectra.

        Returns
        -------
        None.

        """
        fig,ax = plt.subplots()
        wave_index = self.findNearestIndex(wave, self.lambdas)
        ltx = str(mul).count("0")
        unit = ""
        if "/" in labels[0]:
            unit = labels[0].split("/")[1]
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        
        ax.set_xscale("log")
        ax.set_ylabel(labels[2] + dot)
        ax.set_xlabel(labels[1])

        for i in wave_index:
            plt.plot(
                self.delays,
                spectra[i],
                label=str(self.lambdas[i]) + " " + unit
            )
        temp = np.concatenate([spectra[i]
                              for i in wave_index])
        ax.axis(
            [
                min(self.delays),
                max(self.delays),
                1.05 * min(temp),
                1.05 * max(temp)
            ]
        )
        ax.axhline(0, color="black", lw=0.5, alpha = 0.75)
        ax.set_yticks(())
        ax.tick_params(bottom=False)
        ax.legend(loc="upper right", frameon=False, labelcolor="linecolor",
                   handlelength=0)
        plt.savefig(self.path + self.name + "Wavelength_Slices" + ".png")
        
    def plotHeat(self, wave, time, v_min, v_max, spectra, cont, mul, labels, add):
        """
        Plots a subplot with a heatmap of the absorption change in delays
        against lambdas.

        Parameters
        ----------
        wave : list
            Wavelenghts which should be plotted.
        time : list
            Delays which should be plotted.
        v_min : float
            Lower limit for the colorbar.
        v_max : float
            Lower limit for the colorbar.
        spectra : np.array
            Contains the values of the spectra.
        cont : float
            Determines how much contour lines will be shown in the 2D plot.
            High values will show more lines.
        mul : float
            The value by which the spectra will be multiplied.
            The default is 1.
        add : string
            Addition to the title of the subplot.

        Returns
        -------
        None.

        """
        fig, ax = plt.subplots(figsize = (7.6,4))
        ltx = str(mul).count("0")
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        ax.set_yscale("log")
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        A_t = spectra.T*mul
        pcm = ax.pcolormesh(
            self.lambdas,
            self.delays,
            A_t,
            cmap=plt.cm.seismic,
            norm=col.TwoSlopeNorm(vcenter=0, vmin=v_min, vmax=v_max),
            shading="auto",
        )
        if v_min is None:
            v_min = self.setv_min(spectra, mul)
        if v_max is None:
            v_max = self.setv_max(spectra, mul)
        cb = plt.colorbar(pcm)
        cb.set_ticks([v_min, 0, v_max])
        cb.set_label(labels[2] + dot)
        contours = ax.contour(
            self.lambdas,
            self.delays,
            A_t,
            levels=np.arange(v_min, v_max, (1 / cont) * (v_max - v_min)),
            colors="black",
            linewidths=0.7,
            linestyles="solid",
        )
        ax.clabel(contours, inline=False, fontsize=0)

        for i in wave:
            ax.axvline(i,color="black", linestyle="-.")

        for i in time:
            ax.axhline(i, color="black", linestyle="dotted")

        ax.axis(
            [
                min(self.lambdas),
                max(self.lambdas),
                [min(self.delays) if min(self.delays) > 0 else 10 ** (-2)][0],
                max(self.delays),
            ]
        )
        ax.set_xticks
        if "Residuals" in add:
            plt.savefig(self.path + self.name + "Residuals" + ".png")
        else:
            plt.savefig(self.path + self.name + "Heatmap" + ".png")
        
    def plotDSlices(self, time, spectra, mul, labels, add):
        """
        Plots a subplot of absorption change against wavelenghts for chosen
        delays.

        Parameters
        ----------
        time : list
            Delays which should be plotted.
        time_index : list
            Indexes for the delays to be plotted.
        spectra : np.array
            Contains the values of the spectra.

        Returns
        -------
        None.

        """
        fig, ax = plt.subplots()
        time_index = self.findNearestIndex(time, self.delays)
        ltx = str(mul).count("0")
        unit = ""
        if "/" in labels[1]:
            unit = labels[1].split("/")[1]
        dot = ""
        if mul != 1:
            dot = f" $\cdot 10^{ltx}$"
        ax.set_ylabel(labels[2] + dot)
        ax.set_xlabel(labels[0])
        for i in time_index:
            plt.plot(self.lambdas,spectra.T[i], label=str(self.delays[i]) + " " + unit)
        ax.tick_params(bottom=False)
        ax.legend(loc="upper left", frameon=False, labelcolor="linecolor",
                   handlelength=0)
        temp = np.concatenate([spectra.T[i]
                              for i in time_index])
        ax.axis(
            [
                min(self.lambdas),
                max(self.lambdas),
                1.05 * min(temp),
                1.05 * max(temp)
            ]
        )
        ax.set_yticks(())
        ax.axhline(0, color="black", lw=0.5, alpha = 0.75)
        plt.savefig(self.path + self.name + "Delay_Slices" + ".png")