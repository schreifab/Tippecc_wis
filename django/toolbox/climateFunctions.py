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
    
    #datasets
    ds_tas = ClimateDataset("temperature","mean daily temperature",False,"tas")
    ds_sfcwind = ClimateDataset("wind speed","avarege daily windspeed",False,"wind")
    ds_tas_min = ClimateDataset("minimum temperature","minimum daily temperature",False,"tas_min")
    ds_tas_max = ClimateDataset("maximum temperature","maximum daily temperature",False,"tas_min")
    ds_pr = ClimateDataset("precipitation","Daily precipitation",False,"precip")


    #threshold params
    pa_tas_thresh = ClimateParameter("threshold tas","Threshold temperature on which to base evaluation", ['degC', 'K'], [], 'quantified', False)
    pa_sfcwind_thresh = ClimateParameter("threshold wind","Threshold average near-surface wind speed on which to base evaluation", ['m/s'], [], 'quantified', False)
    pa_tas_min_thresh = ClimateParameter("threshold tas min","Threshold temperature on which to base evaluation", ['degC', 'K'], [], 'quantified', False)
    pa_tas_max_thresh = ClimateParameter("threshold tas max","Threshold temperature on which to base evaluation", ['degC', 'K'], [], 'quantified', False)
    pa_pr_thresh = ClimateParameter("threshold pr","Threshold precipitation on which to base evaluation", ['mm/day'], [], 'quantified', False)

    #other params
    pa_freq = ClimateParameter("frequency", "Resampling frequency",[],[],'String', False)
    pa_window = ClimateParameter("window","Minimum number of days to hit the threshold.",[],[],'int',False)
    


    list = [
        ClimateFunction(id=3,name='Calm days', description='The number of days with average near-surface wind speed below threshold (default: 2 m/s).',
            dataset_dict = {
                'sfcWind': ds_sfcwind
            },
            params_dict = {
                'thresh':pa_sfcwind_thresh,
                'freq':pa_freq
            }
        ,climate_func = xclim.indices.calm_days),

        ClimateFunction(id=8,name='Cold spell days', description='The number of days that are part of cold spell events, defined as a sequence of consecutive days with mean dailytemperature below a threshold (default: -10°C).',
            dataset_dict = {
                'tas': ds_tas
            },
            params_dict = {
                'thresh': pa_tas_thresh,
                'window': pa_window,
                'freq': pa_freq,
                'op': ClimateParameter("operator", "Comparison operation", [], ['<', '<=', 'lt', 'le'],'String', False),
                'resample_before_rl': ClimateParameter("do resample before","Determines if the resampling should take place before or after the run length encoding (or a similar algorithm) is applied to runs.",[],["True","False"],"boolean",False)
            }
        ,climate_func = xclim.indices.cold_spell_days),

        
        
        ClimateFunction(id=10,name='Cold spell frequency', description='The number of cold spell events, defined as a sequence of consecutive window dayswith mean daily temperature below a thresh.',
            dataset_dict = {
            'tas': ds_tas
            },
            params_dict = {
            'thresh': pa_tas_thresh,
            'window': pa_window,
            'freq': pa_freq,
            'op': ClimateParameter("operator", "Comparison operation", [], ['<', '<=', 'lt', 'le'],'String', False),
            'resample_before_rl': ClimateParameter("do resample before","Determines if the resampling should take place before or after the run length encoding (or a similar algorithm) is applied to runs.",[],["True","False"],"boolean",False)

            }
            ,climate_func = xclim.indices.cold_spell_frequency),

        ClimateFunction(id=11,name='Longest cold spell', description='Longest spell of low temperatures over a given period.Longest series of at least window consecutive days with temperature at or below thresh.',
        dataset_dict = {
 	 	    'tas': ds_tas
        },
        params_dict = {
            'thresh': pa_tas_thresh,
            'window': pa_window,
            'freq': pa_freq,
            'op': ClimateParameter("operator", "Comparison operation", [], ['<', '<=', 'lt', 'le'],'String', False),
            'resample_before_rl': ClimateParameter("do resample before","Determines if the resampling should take place before or after the run length encoding (or a similar algorithm) is applied to runs.",[],["True","False"],"boolean",False)
        }
        ,climate_func = xclim.indices.cold_spell_max_length),

        ClimateFunction(id=12,name='Total length of cold spells', description='Total length of spells of low temperatures over a given period.Total length of series of at least window consecutive days with temperature at or below thresh.',
        dataset_dict = {
 	 	    'tas': ds_tas
        },
        params_dict = {
            'thresh': pa_tas_thresh,
            'window': pa_window,
            'freq': pa_freq,
            'op': ClimateParameter("operator", "Comparison operation", [], ['<', '<=', 'lt', 'le'],'String', False),
            'resample_before_rl': ClimateParameter("do resample before","Determines if the resampling should take place before or after the run length encoding (or a similar algorithm) is applied to runs.",[],["True","False"],"boolean",False)
        }
        ,climate_func = xclim.indices.cold_spell_total_length),

        ClimateFunction(id=14,name='Cooling degree days', description='Returns the sum of degree days above the temperature threshold at which spaces are cooled',
            dataset_dict = {
                'tas': ds_tas
            },
            params_dict = {
                'thresh': pa_tas_thresh,
                'freq': pa_freq
            }
        ,climate_func = xclim.indices.cooling_degree_days),

        ClimateFunction(id=15,name='Corn heat units', description='Temperature-based index used to estimate the development of corn crops.Formula adapted from :cite:t:`bootsma_risk_1999`.',
            dataset_dict = {
                'tasmin': ds_tas_min,
                'tasmax': ds_tas_max
            },
            params_dict = {
                'thresh_tasmin': pa_tas_min_thresh,
                'thresh_tasmax': pa_tas_max_thresh
            }
        ,climate_func = xclim.indices.corn_heat_units),

        ClimateFunction(id=16,name='Average daily precipitation intensity', description='Return the average precipitation over wet days.Wet days are those with precipitation over a given threshold (default: 1 mm/day).',
            dataset_dict = {
                'pr': ds_pr
            },
            params_dict = {
                'thresh': pa_pr_thresh,
                'freq': pa_freq,
                'op':  ClimateParameter("operator", "Comparison operation", [], ['>', '>=', 'gt', 'ge'],'String', False)
            }
        ,climate_func = xclim.indices.daily_pr_intensity),

        ClimateFunction(id=17,name='Statistics of daily temperature range', description='The mean difference between the daily maximum temperature and the daily minimum temperature.',
            dataset_dict = {
                'tasmin': ds_tas_min,
                'tasmax': ds_tas_max
            
            },
            params_dict = {
                'freq': pa_freq,
                'op':  ClimateParameter("operator", "Reduce operation", [], ['min', 'max', 'mean', 'std'],'String', False)

            }
        ,climate_func = xclim.indices.daily_temperature_range),

        ClimateFunction(id=18,name='variation in daily temperature range', description='Mean absolute day-to-day variation in daily temperature range.',
            dataset_dict = {
                'tasmin': ds_tas_min,
                'tasmax': ds_tas_max
            },
            params_dict = {
                'freq': pa_freq
            }
        ,climate_func = xclim.indices.daily_temperature_range_variability),

        ClimateFunction(id=21,name='Degree-days exceedance date', description='Day of year when the sum of degree days exceeds a threshold (default: 25 K days).Degree days are computed above or below a given temperature threshold (default: 0℃).',
            dataset_dict = {
                'tas': ds_tas
            },
            params_dict = {
                'thresh': pa_tas_thresh,
                'sum_thresh': ClimateParameter("threshold sum","Threshold of the degree days sum", ['degC', 'K'], [], 'quantified', False),
                'after_date': ClimateParameter("after date","Date at which to start the cumulative sum. In MM-DD format, defaults to the start of the sampling period.",[],[],'str',True),
                'freq': pa_freq
            }
        ,climate_func = xclim.indices.degree_days_exceedance_date),

        ClimateFunction(id=23,name='Dry days', description='The number of days with daily precipitation below threshold.',
            dataset_dict = {
                'pr': ds_pr
            },
            params_dict = {
                'thresh': pa_pr_thresh,
                'freq': pa_freq,
                'op': ClimateParameter("operator", "Comparison operation", [], ['<', '<=', 'lt', 'le'],'String', False)
            }
        ,climate_func = xclim.indices.dry_days),

        ClimateFunction(id=24,name='Return the number of dry periods of n days and more', description='Periods during which the accumulated or maximal daily precipitation amount on a window of n days is under threshold.',
            dataset_dict = {
                'pr': ds_pr
            },
            params_dict = {
                'thresh': pa_pr_thresh,
                'window': pa_window,
                'freq': pa_freq,
                'resample_before_rl': ClimateParameter("do resample before","Determines if the resampling should take place before or after the run length encoding (or a similar algorithm) is applied to runs.",[],["True","False"],"boolean",False),
                'op': ClimateParameter("operator", ' Operation to perform on the window. Default is “sum”, which checks that the sum of accumulated precipitation over the whole window is less than the threshold. “max” checks that the maximal daily precipitation amount within the window is less than the threshold. This is the same as verifying that each individual day is below the threshold.', [], ['sum','max'],'String', False)

            }
            ,climate_func = xclim.indices.dry_spell_frequency),
        
        ClimateFunction(id=28,name='Effective growing degree days', description='Growing degree days based on a dynamic start and end of the growing season.',
            dataset_dict = {
                'tasmax': ds_tas_max,
                'tasmin': ds_tas_min
            },
            params_dict = {
                'thresh': pa_tas_min_thresh,
                'method': ClimateParameter('method', 'The window method used to determine the temperature-based start date. For “bootsma”, the start date is defined as 10 days after the average temperature exceeds a threshold. For “qian”, the start date is based on a weighted 5-day rolling average, based on :py:func`qian_weighted_mean_average`.',[],['bootsma','qian'],'str',False),
                'after_date': ClimateParameter("after date",'Date of the year after which to look for the first frost event. Should have the format ‘mm-dd’.',[],[],'str',True),
                'dim': ClimateParameter('dim','Time dimension',[],['time'],'str',False),
                'freq': pa_freq
            }
        ,climate_func = xclim.indices.effective_growing_degree_days),

        ClimateFunction(id=29,name='Extreme intra-period temperature range', description='The maximum of max temperature (TXx) minus the minimum of min temperature (TNn) for the given time period.',
            dataset_dict = {
                'tasmin': ds_tas_min,
                'tasmax': ds_tas_max
            },
            params_dict = {
                'freq': pa_freq
            }
        ,climate_func = xclim.indices.extreme_temperature_range),

        ClimateFunction(id=31,name="first day temperature above", description="First day of temperatures superior to a given temperature threshold",
            dataset_dict = {
                "tas": ds_tas 
                },
            params_dict = {
                "thresh": pa_tas_thresh,
                "op": ClimateParameter("operator", "Comparison operation", [], ['>','>=','gt','ge'],'String', False),
                "after_date": ClimateParameter("date", "Date of the year after which to look for the first event. Should have the format mm-dd",[],[],'String',False),
                "window": pa_window,
                "freq": pa_freq
                },
            climate_func=xclim.indices.first_day_temperature_below),

        ClimateFunction(id=32,name="first day temperature below", description="First day of temperatures inferior to a given temperature threshold",
            dataset_dict = {
                "tas": ds_tas 
                },
            params_dict = {
                "thresh": pa_tas_thresh,
                "op": ClimateParameter("operator", "Comparison operation", [], ['<','<=','lt','le'],'String', False),
                "after_date": ClimateParameter("date", "Date of the year after which to look for the first event. Should have the format mm-dd",[],[],'String',False),
                "window": pa_window,
                "freq": pa_freq
                },
            climate_func=xclim.indices.first_day_temperature_below),
        
        ClimateFunction(id=42,name="growing degree days", description="Growing degree-days over threshold temperature value",
            dataset_dict = {
                "tas": ds_tas
                },
            params_dict = {
                "thresh": pa_tas_thresh,
                "freq": pa_freq
                },
            climate_func=xclim.atmos.growing_degree_days),
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
