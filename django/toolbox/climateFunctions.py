from typing import Any
import xclim.indices
import xarray as xr
import os
import sys

from django.db import models

data_array_names = {
    "tas": 'tas'
}

class ClimateFunction(models.Model):
    """
    Class for all climate function to calculate indices

    Attributes
    ----------
    id: int
        unique identifier
    name: str
        Name of the indices
    description: str
        a short description of the indices
    climate_function: function
        the function wihc calculates the indices
    dataset_dict: {string: ClimateDataset}
        Dict of the Datasets
    params_dict: {string: ClimateParameter}
        Dict of Parameters
    optional_restrictions: boolean
        true if there are any restrictions for optional parameters or datasets
        this parameter is unused yet as there are no such functions implemented.
    scene: ClimateScene
        scenario with aoi and timespan
   
     Methods
    -------
    __init__(self, id, name, description, dataset_dict=None, params_dict=None, climateFunc=None, optional_restrictions=False)
        Construktor
    set_climate_scene(self, scene)
        set Climate scene
    def execute(self, output_path)
        main method for the inices calculation
    get_number_of_datasets_or_error_message(self)
        health check of the data array
    def create_kwargs_dict(self, i):
        create kwargs to call the climate_function
    """
    
    id = models.IntegerField
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    climate_function = models.Func
   
    def __init__(self, id, name, description, dataset_dict=None, params_dict=None, climateFunc=None, optional_restrictions=False):
        """
        Constructor
        """
        
        self.id = id
        self.name = name
        self.description = description
        self.dataset_dict = dataset_dict
        self.params_dict = params_dict
        self.climate_function = climateFunc
        self.optional_restrictions=optional_restrictions
        
    def set_climate_scene(self, scene): 
        """set Climate scene

        Args:
            scene: ClimateScene
                scenario with aoi and timespan
        """
        self.scene = scene

    def execute(self, output_path): 
        """Executes the function (attribute climate_function) for every data file

        Args:
            output_path: str
                folder path for the location where the results should be stored

        Returns:
            str
                message
            [str]
                array of results as path list
        """
        message = "Function was executed succesfully"
        results = []
        # number of ds will return the amount of data to iterate or an error message
        number_of_datasets = self.get_number_of_datasets_or_error_message()
        if type(number_of_datasets) is not int:
            # if error message: return
            return number_of_datasets, results
        for i in range(number_of_datasets):
            try:
                result_ds = self.climate_function(**self.create_kwargs_dict(i))
            except Exception as e:
                message = str(e)
                return message, results
            output_filename = self.name + "_" + str(i)
            result_ds.to_netcdf(os.path.join(output_path, output_filename))
            results.append(output_filename)
        return message, results

    def get_number_of_datasets_or_error_message(self):
        number_of_datasets = 0
        for key in self.dataset_dict:
            length = len(self.dataset_dict[key].path_list)
            if (length == 0 and self.dataset_dict[key].optional == False):
                return "No dataset found"
            if (number_of_datasets == 0):
                number_of_datasets = length
            if ((number_of_datasets != length and self.dataset_dict[key].optional == False) or (number_of_datasets != length and self.dataset_dict[key].optional == True and length != 0)):
                return "different amount of datasets were found. Unable to execute"
        return number_of_datasets
    
    def create_kwargs_dict(self, i):
        kwargs = {}
        for key in self.dataset_dict:
            kwargs[key] = getattr(clip_ds_by_scene(self.dataset_dict[key].get_dataset(i), self.scene),data_array_names[key]) #remove tas here later
        for key in self.params_dict:
            kwargs[key] = self.params_dict[key].value
        print(kwargs)
        return kwargs

class ClimateDataset(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    filter_word = models.CharField(max_length=100)
    optional = models.BooleanField(editable = False, help_text = "True if dataset is optional")

    def __init__(self, name, desc, filter_word, optional):
        self.name = name
        self.desc = desc
        self.filter_word = filter_word
        self.optional = optional
        
    def set_path_list(self, path_list):
        self.path_list = path_list
        
    def get_dataset(self, i):
        ds = xr.open_dataset(self.path_list[i], engine = 'netcdf4')
        #remove if data correct
        ds.tas.attrs['units'] = 'K'
        return ds


class ClimateParameter(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    input_list = []
    unit_list = []
    datatype = models.CharField(max_length=100)
    optional = models.BooleanField(editable = False, help_text = "True if parameter is optional")

    def __init__(self, name, desc, unit_list, input_list, datatype, optional):    
        self.name = name
        self.desc = desc
        self.input_list = input_list
        self.unit_list = unit_list
        self.datatype = datatype
        self.optional = optional
        
    def set_value(self, value):
        if self.datatype == "float":
            self.value = float(value)
        # add more elif statements here if other datatype transformations are needed
        else: 
            self.value = value
        
        
class ClimateFunctionList:
    list = [ClimateFunction(id=1,name="growing degree days", description="Growing degree-days over threshold temperature value",
                            dataset_dict = {
                                "tas": ClimateDataset("temperature","mean daily temperature","none",False)
                                },
                            params_dict = {
                                "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['degC', 'K'],[], 'String', False),
                                "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
                                },
                            climateFunc=xclim.atmos.growing_degree_days),
            ClimateFunction(id=2,name="first day temperature below", description="First day of temperatures inferior to a given temperature threshold",
                            dataset_dict = {
                                "tas": ClimateDataset("temperature","mean daily temperature","none",False)
                                },
                            params_dict = {
                                "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['degC', 'K'], [], 'String', False),
                                "op": ClimateParameter("operator", "Comparison operation", [], ['<', '<=', 'lt', 'le'],'String', False),
                                "after_date": ClimateParameter("date", "Date of the year after which to look for the first event. Should have the format mm-dd",[],[],'String',False),
                                "window": ClimateParameter("window","Minimum number of days with temperature below threshold needed for evaluation.",[],[],'int',False),
                                "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
                                },
                            climateFunc=xclim.indices.first_day_temperature_below)
            ]
    
    def get_func_by_id(self, id):
        for func in self.list:
            if func.id == id:
                return func
        return 0

class ClimateScene():
    
    def __init__(self, aoi, time_min = '1970-01-01T12:00:00.000000000', time_max  = '2100-12-31T12:00:00.000000000'):
        self.lon_min = aoi[0]
        self.lon_max = aoi[1]
        self.lat_min = aoi[2]
        self.lat_max = aoi[3]
        self.time_min = time_min
        self.time_max = time_max

class ClimateFunctionRequest(models.Model):
    dataset_list = []
    paramvalue_dict = {}
    aoi = []
    def __init__(self, dataset_list, paramvalue_dict) :
        self.dataset_list = dataset_list
        self.paramvalue_dict = paramvalue_dict

class ExecuteResponse(models.Model):
    message =  models.CharField(max_length=200)
    id = models.IntegerField
    def __init__(self,id, message):
        self.message = message
        self.id = id
        
def clip_ds_by_scene(ds, scene):
    return ds.sel(lon=slice(scene.lon_min, scene.lon_max), lat=slice(scene.lat_min, scene.lat_max), time=slice(scene.time_min,scene.time_max))
