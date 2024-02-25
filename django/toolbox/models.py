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
        Constructor
    set_climate_scene(self, scene)
        set Climate scene
    def execute(self, output_path)
        main method for the inices calculation
    get_number_of_datasets_or_error_message(self)
        health check of the data array
    create_kwargs_dict(self, i)
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
        print("test")
        # number of ds will return the amount of data to iterate or an error message
        number_of_datasets = self.get_number_of_datasets_or_error_message()
        
        if type(number_of_datasets) is not int:
            # if error message: return
            return number_of_datasets, results
        collection_ids = self.get_collection_ids_or_error_message()
        if type(collection_ids) is str:
            return collection_ids, results
        print(collection_ids)
        for id in collection_ids:
            try:
                result_ds = self.climate_function(**self.create_kwargs_dict(id))
                output_filename = self.name + "_" + str(id)
                result_ds.to_netcdf(os.path.join(output_path, output_filename))
            except Exception as e:
                message = str(e)
                return message, results
            results.append(output_filename)
        return message, results

    def get_number_of_datasets_or_error_message(self):
        """
        Health check for the given Dataset pathes. 
        Checks the following:
        The array for all datasets must have the sam lenght (Exception: Optional ds could be zero)
        All non-optional ds must have at lest one entry.
        Coul return eithe the amount of ds or an error message
        
        Returns:
            str | int:
                Error message or number of ds
        """
        number_of_datasets = 0
        for key in self.dataset_dict:
            length = len(self.dataset_dict[key].path_dict)
            if (length == 0 and self.dataset_dict[key].optional == False):
                return "No dataset found"
            if (number_of_datasets == 0):
                number_of_datasets = length
            if ((number_of_datasets != length and self.dataset_dict[key].optional == False) or (number_of_datasets != length and self.dataset_dict[key].optional == True and length != 0)):
                return "different amount of datasets were found. Unable to execute"
        return number_of_datasets
    
    def get_collection_ids_or_error_message(self):
        """
        Health check for the given Dataset collection ids. 
        Checks the following:
        the ids of all dataset used must be the same
        returns the collection id list for iteration or error message

        Returns:
            str | [str]:
                Error message or id list
        """
        id_list = []
        for key in self.dataset_dict:
            if len(id_list) == 0:
                id_list = list(self.dataset_dict[key].path_dict.keys())
            else: 
                compare_list = list(self.dataset_dict[key].path_dict.keys())
                #optional might be zero
                if len(compare_list) > 0: 
                    if set(id_list) != set(compare_list):
                        return "Data error: Not the same collections for the datasets found"
        return id_list





    def create_kwargs_dict(self, id):
        """
        create the argument dictionary that will be passed into the flexible climate function

        Args:
            i: int
                The elememnt position for the dataset array. 
                This is nescasarry as the function has to be called for every ds.

        Returns:
            {str: xarray.dataset | str | int | float}
                kwargs dict
        """
        kwargs = {}
        for key in self.dataset_dict:
            if len(self.dataset_dict[key].path_dict) > 0:
                kwargs[key] = getattr(clip_ds_by_scene(self.dataset_dict[key].get_dataset(id), self.scene),data_array_names[key]) 
        for key in self.params_dict:
            kwargs[key] = self.params_dict[key].value
        print(kwargs)
        return kwargs

class ClimateDataset(models.Model):
    """
    Class for the Dataset. Each Object ClimateFunction might have n ClimateDatasets
    ClimateDataset represents the type of the ds (e.g. tas, precip). Each type might have multiple files for the data
    

    Attributes
    ----------
    name: str:
        the name of the ds
    desc: str
        a short description 
    filter_word: str
        was planned as a filter option. Is unused yet. Might be removed
    optional: boolean
        true if the dataset is optional. ds will be checkable in ui and the function works without it 
    path_list: [str]
        list of paths for the files
    
    Methods
    -------
    __init__(self, name, desc, filter_word, optional)
        Constructor
    set_path_list(self, path_list)
        sets the paths list
    get_dataset(self, i)
        opens and returns the ds for the path list on i
    """
    
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    filter_word = models.CharField(max_length=100)
    optional = models.BooleanField(editable = False, help_text = "True if dataset is optional")

    def __init__(self, name = name, desc = desc, optional = optional, filter_word = filter_word):
        """
        Constructor
        """
        self.name = name
        self.desc = desc
        self.filter_word = filter_word
        self.optional = optional
        self.path_dict = []
        
    def set_path_dict(self, path_dict):
        """
        sets path list. 
        As pathlist is currently a public attribute, this function could be replaced
        However, it is possible to implement a more complex function here

        Args: 
            path_list: [str]
                list of paths for the files
        """
        self.path_dict = path_dict
        
    def get_dataset(self, id):
        """
        Open the dataset for the path_list on position i

        Args:
            i: int
                position for path_list

        Returns:
            xarray.dataset
                the open dataset that will be used for the calculation
        """
        print(self.path_dict[id])
        ds = xr.open_dataset(self.path_dict[id], engine = 'netcdf4')
        #remove if data correct
        #ds.tas.attrs['units'] = 'K'
        return ds


class ClimateParameter(models.Model):
    """
    Class for Parameter Options for a ClimateFunction.
    Each Object ClimateFunction might have n ClimateParameter.
    

    Attributes
    ----------
    name: str:
        the name of the ds
    desc: str
        a short description 
    input_list: [str]
        Is used if there strict options for the input. In that case there will be a option list in ui.
        Could be void if there are no option (e.g. for numbers). I that case there will be a input form in ui.
    unit_list: [str]
        Is used, if an additional unit is needed for the input field.
        Could be void if there are no units.
    datatype: str
        The datatype of the value as function argument. Is determinated by function requirements
        currently int, float, str are implemented.
    optional: boolean
        true if the parameter is optional.
    value: Any
        The chosen value, that will be passed as param to the climate_function.

    Methods
    -------
    __init__(self, name, desc, unit_list, input_list, datatype, optional)
        Constructor
    set_value(self, value)
        set value and perform data transformation

    """
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    input_list = []
    unit_list = []
    datatype = models.CharField(max_length=100)
    optional = models.BooleanField(editable = False, help_text = "True if parameter is optional")

    def __init__(self, name, desc, unit_list, input_list, datatype, optional):    
        """
        Constructor
        """
        self.name = name
        self.desc = desc
        self.input_list = input_list
        self.unit_list = unit_list
        self.datatype = datatype
        self.optional = optional
        
    def set_value(self, value):
        """
        set value and perform data transformation to datatype (attribut of th class)
        Args:
            value: any
                the value selected by the user
        """
        if self.datatype == "float":
            self.value = float(value)
        if self.datatype == "string" or self.datatype == "str":
            self.value = str(value)
        if self.datatype == "int" or self.datatype == "integer":
            self.value = int(value)
        # add more elif statements here if other datatype transformations are needed
        else: 
            self.value = value
        
        

class ClimateScene():
    """
    Interface for the scenario
     
    Attributes
    ----------
    aoi: [float]
        [lat min, lat max, lon min, lon max]
    time_min: str
        startdate in format yyyy-mm-dd (+ time)
    time_max: str
        enddate in format yyyy-mm-dd (+ time)
    """
    def __init__(self, aoi, time_min = '1970-01-01T12:00:00.000000000', time_max  = '2100-12-31T12:00:00.000000000'):
        self.lon_min = aoi[0]
        self.lon_max = aoi[1]
        self.lat_min = aoi[2]
        self.lat_max = aoi[3]
        self.time_min = time_min
        self.time_max = time_max

class ClimateFunctionRequest(models.Model):
    """
    Not a `real` class, just a model for request. 
    See api documentation for more.
    """
    dataset_list = []
    paramvalue_dict = {}
    aoi = []
    file_id_list = []
    def __init__(self, dataset_list, paramvalue_dict) :
        self.dataset_list = dataset_list
        self.paramvalue_dict = paramvalue_dict

class ExecuteResponse(models.Model):
    """
    Not a `real` class, just a model for request. 
    See api documentation for more.
    """
    message =  models.CharField(max_length=200)
    id = models.IntegerField
    def __init__(self,id, message):
        self.message = message
        self.id = id
        
def clip_ds_by_scene(ds, scene):
    """
    uses the slice function of xarray to cut a ds by time and aoi.

    Args:
        ds: xarray.dataset
            the data
        scene: ClimateScene
            scenario
    Returns:
        xarray.dataset
            clipped data as new ds
    """
    return ds.sel(lon=slice(scene.lon_min, scene.lon_max), lat=slice(scene.lat_min, scene.lat_max), time=slice(scene.time_min,scene.time_max))
