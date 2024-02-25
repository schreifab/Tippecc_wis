from toolbox.models import ClimateFunction,ClimateDataset,ClimateParameter
import xclim

class ClimateFunctionList:
    """
    Container for the implemented functions
    
    Attributes
    ----------
    list: [ClimateFunction]
        list of all implemented functions
        
    Methods
    -------
    get_func_by_id(self, id)
        searching a function by its id
    """
    
    ds_tas = ClimateDataset("temperature","mean daily temperature",False,"none")

    list = [ClimateFunction(id=1,name="growing degree days", description="Growing degree-days over threshold temperature value",
                            dataset_dict = {
                                "tas": ds_tas
                                },
                            params_dict = {
                                "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['degC', 'K'],[], 'quantified', False),
                                "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
                                },
                            climateFunc=xclim.atmos.growing_degree_days),
            ClimateFunction(id=2,name="first day temperature below", description="First day of temperatures inferior to a given temperature threshold",
                            dataset_dict = {
                                "tas": ds_tas 
                                },
                            params_dict = {
                                "thresh": ClimateParameter("threshold","Threshold temperature on which to base evaluation", ['degC', 'K'], [], 'quantified', False),
                                "op": ClimateParameter("operator", "Comparison operation", [], ['<','<=','lt','le'],'String', False),
                                "after_date": ClimateParameter("date", "Date of the year after which to look for the first event. Should have the format mm-dd",[],[],'String',False),
                                "window": ClimateParameter("window","Minimum number of days with temperature below threshold needed for evaluation.",[],[],'int',False),
                                "freq": ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
                                },
                            climateFunc=xclim.indices.first_day_temperature_below)
            ]
    
    
    def get_func_by_id(self, id):
        """
        returning a function by its id from list

        Args:
            id: int
                search id

        Returns:
            Climate Function
        """
        for func in self.list:
            if func.id == id:
                return func
        return 0
