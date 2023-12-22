import xclim.indices
import xarray as xr

from django.db import models

class ClimateFunction(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    climateFunction = models.Func
   
    def __init__(self, id, name, description, dataset_dict=None, params_dict=None, climateFunc=None, optional_restrictions=False):
        self.id = id
        self.name = name
        self.description = description
        self.dataset_dict = dataset_dict
        self.params_dict = params_dict
        self.climateFunction = climateFunc
        self.optional_restrictions=optional_restrictions

    def execute(self): 
        return self.climateFunction(**self.dataset_dict, **self.params_dict)

class ClimateDataset(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    filter_word = models.CharField(max_length=100)
    optional = models.BooleanField

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


class ClimateParameter(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    input_list = []
    unit_list = []
    datatype = models.CharField(max_length=100)
    optional = models.BooleanField

    def __init__(self, name, desc, unit_list, input_list, datatype, optional):    
        self.name = name
        self.desc = desc
        self.input_list = input_list
        self.unit_list = unit_list
        self.datatype = datatype
        self.optional = optional

class ClimateFunctionList:
    list = [ClimateFunction(id=0,name="growing degree days", description="Growing degree-days over threshold temperature value",
                            dataset_dict = {
                                "tas": ClimateDataset("temperature","mean daily temperature","none",False)
                                },
                            params_dict = {
                                "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['degC', 'K'],[], 'String', False),
                                "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
                                },
                            climateFunc=xclim.atmos.growing_degree_days),
            ClimateFunction(id=1,name="growing degree days", description="Growing degree-days over threshold temperature value",
                            dataset_dict = {
                                "tas": ClimateDataset("temperature","mean daily temperature","none",False)
                                },
                            params_dict = {
                                "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['degC', 'K'], [], 'String', False),
                                "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
                                },
                            climateFunc=xclim.atmos.growing_degree_days)
            ]
