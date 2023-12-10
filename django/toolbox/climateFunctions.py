import xclim.indices
import xarray as xr

class ClimateFunction():
    def __init__(self, dataset_dict, params_dict):
        self.dataset_dict = dataset_dict
        self.params_dict = params_dict
    
        
        
class ClimateDataset(): 
    def __init__(self, name, desc, filter_word, optional):
        self.name = name
        self.desc = desc
        self.filter_word = filter_word
        self.optional = optional
        
    def set_path(self, path):
        self.path = path
        
    def get_dataset(self):
        ds = xr.open_dataset(self.path, engine = 'netcdf4')
        #remove if data correct
        ds.tas.attrs['units'] = 'K'
        return ds

class ClimateParameter():
    def __init__(self, name, desc, unit_list, input_list, datatype, optional):    
        self.name = name
        self.desc = desc
        self.input_list = input_list
        self.unit_list = unit_list
        self.datatype = datatype
        self.optional = optional
        
    

class GrowingDegreeDays(ClimateFunction): 
    optional_restrictions = False
    name = "growing degree days"
    description = "Growing degree-days over threshold temperature value"
    def __init__(self):
        dataset_dict = {
            "tas": ClimateDataset("temperature","mean daily temperature","none",False)
            }
        params_dict = {
            "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['deGC'],[], 'String', False),
            "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
            }
        super().__init__(dataset_dict, params_dict)
        
    
    def execute(self): 
        return xclim.atmos.growing_degree_days(tas=self.dataset_dict["tas"].get_dataset().tas, thresh="10.0 degC", freq="MS")


class ClimateFunctionList:
    list = [GrowingDegreeDays]
