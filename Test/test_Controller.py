import os,sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)  
import pytest as pt
from Controller import Controller
import numpy as np

class TestClassModel:

    con = Controller("D:\发射光谱处理\EfsTA")
    
class Test_init(TestClassModel):
    def setup(self):
        self.csv_filename="D:\发射光谱处理\EfsTA\Test\TA_Average.csv"

    def test_type(self):
        #assert [type(self.con.delays_filename),
        #        type(self.con.spectra_filename),
        #        type(self.con.lambdas_filename)] == [str, str, str]
        assert type(self.con.csv_filename) == str

    def test_values(self):
        assert self.con.csv_filename == self.csv_filename
    
    # def test_values_delays(self):
    #     assert self.con.delays_filename == self.delays_filename
        
    # def test_values_spectra(self):
    #     assert self.con.spectra_filename == self.spectra_filename
        
    # def test_values_lambdas(self):
    #     assert self.con.lambdas_filename == self.lambdas_filename
        
class Test_calcDAS(TestClassModel):
    def setup(self):
        preparam = [(1.2,True),(160,True),(900000,False)]
        d_limits = [0.3, None]
        l_limits = [None, None]
        opt_method = "Nelder-Mead"
        self.tau_fit, self.spec, self.res, D_fit, fit_report = self.con.calcDAS(preparam, d_limits,
                                                        l_limits, opt_method)
        
    def test_type(self):
        assert [type(self.tau_fit), type(self.spec),
                type(self.res)] == [list, np.ndarray, np.ndarray]
        
    def test_shape(self):
        assert [len(self.tau_fit), self.spec.shape,
                self.res.shape] == [3, (366, 107), (366, 107)]
        
class Test_calcSAS(TestClassModel):
    def setup(self):
        K = []
        preparam = [(1.2,True),(160,True),(900000,False)]
        C_0 = []
        d_limits = [0.3, None]
        l_limits = [None, None]
        model = 1
        tau_low = [None,None,None]
        tau_high = [None,None,None]
        opt_method = "Nelder-Mead"
        ivp_method = "BDF"
        self.k_fit, self.spec, self.res,  D_fit, fit_report = self.con.calcSAS(K, preparam, C_0, d_limits, l_limits, model, tau_low, tau_high, opt_method, ivp_method)
        
    def test_shape(self):
        assert [len(self.k_fit), self.spec.shape,
                self.res.shape] == [3, (366, 107), (366, 107)]
        
    def test_type(self):
        assert [type(self.k_fit), type(self.spec),
                type(self.res)] == [list, np.ndarray, np.ndarray]