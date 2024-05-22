## SMART (Single-column Multi-layered Atmospheric Radiative Transfer) Model
---
### How to install the Model
You can download and install the model via the following steps.
1. Prepare the prerequirements of the python environment.
    * Download and install python 3.10.12 into your machine.
    * Using pip3 install the follwoing modules into your python environment.
        * Numpy 1.26.3
        * Matplotlib 3.8.2
        * PyYAML 5.4.1
        * Xarray 2023.12.0
        * Pickle 4.0
        * netCDF4 1.6.5
    * The model may work or do not work properlly based on the python environment. But we've tested our model in the above python environment, therefore it is ensured that the model works well for that.
2. Download this model via Release Section of the Github repository. (Make sure to download the last release!)
3. Unpack the zip to local directory, and access that directory via cmd (Windows) or a shell (Linux/Unix).
4. All Done!

### How to run the Model
1. Prepare Initial Profile TXT Files in somewhere of your directory (Density, SW/LW Absorvity, R, cp, Initial Temperature)
2. Edit config.yml Configuration Manifest File to match up your specification.
3. In command line, use python3 Interpreter to run src/main.py with the path to config.yml as the first argument.

### About Profile TXT
* Put value of the physical quantities in each line.
* Note that the first line corresponds to the quantity of the lowest height, and the last line corresponds to the quantity of the highest height.
* Keep in mind only initial temperature profile txt file should be nz-lined file.
* All other profile txt files should have nz-1 lines.

### Configuration File Guide (`config.yml`)
* The configuration file, located in `src/config.yml` has the followig two sections.
    1. ModelIOConfig
    2. ModelStructureConfig
* The detailed information of the fields can be found in below, or comments in the `src/config.yml`.
* You can copy the default configuration file, `src/config.yml` to somewhere, modify it as you want, and run this model by giving the path to that configuration file as the first argument for the driver script.

#### ModelIOConfig Section
* **configPath**: The path to the configuration file. (Not actually used in the model)
* **cPProfilePath**: The path to the $c_{p}$ profile of the atmosphere txt file.
* **RProfilePath**: The path to the $R$ profile of the atmosphere txt file.
* **aSwProfilePath**: The path to shortwave (less than 4 micrometer) absorptivity profile of the atmosphere txt file.
* **aLwProfilePath**: The path to longwave (more than 4 micrometer) absorptivity profile of the atmosphere txt file.
* **initTProfilePath**: The path to temperature profile txt file, of the atmosphere at the initial timestep.
* **densityProfilePath**: The path to atmospheric density profile txt file.
* **outputPath**: The path of the directory where the output of the model goes into.

#### ModelStructureConfig Section
* **filter**: Uppercase-only string that indicates which equilibrium-detecting(maintaining) filter will be used in the model. For an detailed information, refer to the 'About Filters' Section of this documentation. Can have the value among the following five options:
    * *NONE* - Do not use the equilibrium-detecting filter.
    * *RT* - Use radiation flux sign change-based equilibrium-detecting filter.
    * *TEMP* - Use temperature-delta sign change-based equilibrium-detecting filter.
    * *BOTH* - Use both radiation flux sign change-based equilibrium-detecting filter and the temperature-delta sign change-based one.
    * *FORWARD* - (Temporary for the v0.1 and will be removed later) Use forward-euler time integration fdm scheme instead of the default trapezoidal scheme, to prevent oscilliations in the solution.
* **tolerationCount**: An integer greater than or equal to zero, which indicates how many times should the filter module will tolerate for the sign changes (oscilliations).
* **solarConstantIncident**: The incident solar constant value. in W/m2.
* **dz**: The vertial length of the cell in this model. in m.
* **dt**: The time gap between two timesteps in this model, in s.
* **dx**: The horizontal length of the cell along the longitudal-direction in this model. in m.
* **dy**: The horizontal length of the cell along the latitudual-direction in this model. in m.
* **nz**: The total number of the vertical-layer, including surface layer. Must be greater than or equal to 2.
* **nt**: The total number of the timesteps, including initial timestep. Must be greater than or equil to 1.
* **Csua**: The heat capacity of the surface, PER UNIT AREA. in J/Km2

### About 'Filters'
* The filter in this model is used for detecting whether the layer of this model reached thermodynamical equilibirum-state or not.
* By the default, we're using trapezoidal fdm scheme for the time integration in this model, therefore it is inevitable to confront the situation that, around equilibrium the solution oscilliates and highly disturbs all other layer calculations in our model.
* Therefore we decided to use some filter modules, to detecting equilbirum-reached layers roughly and preventing them from the further radiative updates for the stability.
* We provide two filter modules for our model, RTFilter and TempFilter. Both of them are based on the same mechanisms as following:
    1. Check the sign of the specific quantities of every layer, is opposite to the ones of the previous timestep.
    2. If so, count as violations of the layer.
    3. If a violation count of the layer exceeds the toleratation count, than prevent all further updates toward that layer, also mark oscilliated temperature fields as their arithmetical mean.
* RTFilter works based on the sign changes of the radiative net flux of that layer, while TempFilter works based on the changes of the temperature-delta (current temperature of the layer - previous temperature of the layer)
* (Temporary for the v0.1) In version 0.1, we also provide 'FORWARD' option to the filter field. Note this is temporary addition. We'll move this option to an independent option field that allows user to select their time fdm integration method. If you select this 'filter (not actually filter, it is rather an fdm-selecting option)' the model will use forward-euler time fdm instead of the basic trapezoidal one.
    * This option will be great for preventing oscilliations in the solution, but using this option the solution will be monotonically increasing or decreasing one instead.
    * In version 0.1 we did not add the equilibrium-detecting algorithms for the monotonical increasing/decreasing solutions from forward-euler fdm scheme, so please keep this in your mind.

### About Outputs
* For every run of this model, you will find out the result in the `outPath` that you've specified in the configuration file.
* Every model run generates two output files with the timestamp of the model run:
    1. A single python pickle file: `result_modelData_timestamp.pkl`
    2. A NetCDF4 file: `result_temperature_timestamp.nc`
* The first output file, the python pickle file contains all information about a single model run, including its configurations, the data used in the model and the final temperature output.
    * This file is just a serialization of the `common.datastructures.ModelResult` dataclass, therefore you can just load the file via python Pickle module in python environment, and read it. (Note. before this you should import `common.datastructures` into your environment.
* The second output file, the NetCDF4 file contains the temperature profiles among all timesteps in the model run, with proper explanations and the coordinates.
    * You can load and read this file via python xarray module or something-other modules like that. Refer internet documentations for more information.
