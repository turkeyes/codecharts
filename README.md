# CodeCharts

A scalable, natural alternative to eye-tracking that can be deployed as a crowdsourced task. It uses a self-report methodology to determine where on an image a participant was looking. 

A running web demo of this interface is available here: http://turkeyes.mit.edu/codecharts/

If you use this code, please consider citing:

> Newman, A., McNamara, B., Fosco, C., Zhang, Y.B., Sukhum, P., Tancik, M., Kim, N.W., Bylinskii, Z. [TurkEyes: A Web-Based Toolbox for Crowdsourcing Attention Data.](http://turkeyes.mit.edu/) In ACM CHI, 2020.

> Rudoy, D., Goldman, D. B., Shechtman, E., & Zelnik-Manor, L. [Crowdsourcing gaze data collection.](https://arxiv.org/abs/1204.3367) In Proc. Collective Intelligence, 2012.

## Getting started

1. Clone this repository. All the experimental files have been pre-generated for a sample task in [assets/task_data](https://github.com/turkeyes/codecharts/tree/master/assets/task_data). 
2. To test the interface with this sample task, change to the main repo directory where the index.html file is located, and run a local http server of your choice, i.e., run this command in your terminal:

`python3 -m http.server`

3. Take your web browser to http://localhost:8000/ and try the task! 

## Testing on your own data

Using the interface for your own data collection requires two steps: 1) generating input data to the interface and 2) configuring the webpage to your needs. 

### Generating input data

The iPython notebook found at [generate-experiment-files/main.ipynb](https://github.com/turkeyes/codecharts/blob/master/generate-experiment-files/main.ipynb) should walk you step-by-step through generating all the experimental files required to run the CodeCharts interface with a new set of images. You will provide the path to the directory hosting these images and be able to further customize the experimental design (choosing the tutorial and sentinel images, the experiment length, and the number of subject files to generate). The code will output all the files to [assets/task_data](https://github.com/turkeyes/codecharts/tree/master/assets/task_data), and you can test the interface with the new images by repeating step 2 (from "Getting started"). Each time the page is refereshed, a new subject file will be preloaded. 

### Configuring the webpage

Configure the interface to your needs as follows: 

1. Open the file `assets/js/custom.js`. This is the principal JavaScript file responsable for the interface logic. At the top of the file there is a section labeled "UI Parameters" that contains configurable parameters that change how the task runs. Change the variables `N_BUCKETS` and `N_SUBJ_FILES` to match the number of buckets and subject files, respectively, that you generated above. To make sure the JavaScript can find your input data, either ensure that your data is in the file `assets/task_data` or change the variables `DATA_BASE_PATH` and `IMAGE_BASE_PATH`. 
2. Change the variables `NUM_MSEC_CROSS`, `NUM_MSEC_IMAGE`, `NUM_MSEC_SENTINEL`, and `NUM_MSEC_CHAR` to change how long the fixation cross, target images, sentinel images, and codecharts are shown to the participant. Adjust any other variables in the "UI Parameters" section that you desire.
3. Edit the file `config.json` to customize the task title, instructions, and disclaimer. You can also set the boolean `advanced.includeDemographicSurvey` to include a demographic survey at the end of the task, and you can set `advanced.hideIfNotAccepted` to block continuing with the task if it is on MTurk and the worker has not accepted the task. 
4. Decide how you want to host the collected task data.
  * Configure a back-end to store your data. The interface works out-of-the-box as an MTurk `ExternalQuestion`. Please see https://github.com/a-newman/mturk-api-notebook for an example of how to deploy the task on MTurk once all the experimental files have been hosted on a public webpage. 
  * If you are not using MTurk and/or you want to use your own back-end to store data, set the variable `advanced.externalSubmit` in `config.json` to `true` and change `externalSubmitUrl` to the url that you would like to `POST` data to instead. With this configuration, the interface will expect a json response of the form `{"key": <submit_code>}`. The submit code will be shown to the user on completion. 
  * Alternatively, the https://github.com/turkeyes/codecharts/tree/print_data branch of this repository contains a version that downloads the collected data from the task to a local file. You can use this to test your task before launching it with a back-end, or you can use this as-is to collect data with local participants.

## Table of Contents

* `config.json`: configuration files containing general task-setup parameters. 
* `index.html`: main html file for the interface 
* `assets/`: contains JavaScript files and input data for the interface as well as some additional libraries and assets. Important files detailed below: 
    * `js/custom.js`: JS file containing all task-specific logic. Most changes you make to the interface should involve this file. 
    * `js/main.js`: generic file handling task flow, data submission, etc. Does not contain task-specific logic. 
    * `task_data`: default folder for storing task input data.
