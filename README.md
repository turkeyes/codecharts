# CodeCharts

A scalable, natural alternative to eye-tracking. 

## Getting started

You can test the interface by running a local http server of your choice. For instance: 

`python3 -m http.server`

We have configured the interface with some pre-prepared images and code charts so that you can see how it works. 

## Testing on your own data

Using the interface for your own data collection requires two steps: 1) generating input data to the interface and 2) configuring the webpage to your needs. 

### Preparing the task data

The CodeCharts interface expects input task data in a specific format. We have provided code that takes in a folder of target images and a few other parameters and outputs the data expected by the CodeCharts interface. To generate the input data, see the Jupyter notebook `generate-experiment-files/main.ipynb`. 

### Configuring the webpage

Configure the interface to your needs as follows: 

1. Open the file `assets/js/custom.js`. This is the principal JavaScript file responsable for the interface logic. At the top of the file there is a section labeled "UI Parameters" that contains configurable parameters that change how the task runs. Change the variables `N_BUCKETS` and `N_SUBJ_FILES` to match the number of buckets and subject files, respectively, that you generated above. To make sure the JavaScript can find your input data, either ensure that your data is in the file `assets/task_data` or change the variables `DATA_BASE_PATH` and `IMAGE_BASE_PATH`. 
2. Change the variables `NUM_MSEC_CROSS`, `NUM_MSEC_IMAGE`, `NUM_MSEC_SENTINEL`, and `NUM_MSEC_CHAR` to change how long the fixation cross, target images, sentinel images, and codecharts are shown to the participant. Adjust any other variables in the "UI Parameters" section that you desire.
3. Edit the file `config.json` to customize the task title, instructions, and disclaimer. You can also set the boolean `advanced.includeDemographicSurvey` to include a demographic survey at the end of the task, and you can set `advanced.hideIfNotAccepted` to block continuing with the task if it is on MTurk and the worker has not accepted the task. 
4. Configure a back-end to store your data. The interface works out-of-the-box as an MTurk `ExternalQuestion`. If you are not using MTurk and/or you want to use your own back-end to store data, set the variable `advanced.externalSubmit` in `config.json` to `true` and change `externalSubmitUrl` to the url that you would like to `POST` data to instead. With this configuration, the interface will expect a json response of the form `{"key": <submit_code>}`. The submit code will be shown to the user on completion. 

## Table of Contents

* `config.json`: configuration files containing general task-setup parameters. 
* `index.html`: main html file for the interface 
* `assets/`: contains JavaScript files and input data for the interface as well as some additional libraries and assets. Important files detailed below: 
    * `js/custom.js`: JS file containing all task-specific logic. Most changes you make to the interface should involve this file. 
    * `js/main.js`: generic file handling task flow, data submission, etc. Does not contain task-specific logic. 
    * `task_data`: default folder for storing task input data.
