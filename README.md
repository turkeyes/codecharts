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

The iPython notebook at [generate-experiment-files/main.ipynb](https://github.com/turkeyes/codecharts/blob/master/generate-experiment-files/main.ipynb) will walk you step-by-step through generating the experiment files required to run the interface with a new set of images. You will:
- provide a directory of images on which you wish to collect attention data
- customize the experimental design by choosing tutorial and sentinel images, the experiment length, and the number of subject files to generate 
- output your experiment files to [assets/task_data](https://github.com/turkeyes/codecharts/tree/master/assets/task_data). Once this is done, you can test your experiment by repeating step 2 (from "Getting started").

### Configuring the webpage

Configure the interface to your needs as follows: 

1. Open the file `assets/js/custom.js`. This is the principal JavaScript file responsable for the interface logic. At the top of the file there is a section labeled "UI Parameters" that contains configurable parameters that change how the task runs. Change the variables `N_BUCKETS` and `N_SUBJ_FILES` to match the number of buckets and subject files, respectively, that you generated above. To make sure the JavaScript can find your input data, either ensure that your data is in the file `assets/task_data` or change the variables `DATA_BASE_PATH` and `IMAGE_BASE_PATH`. 
2. Change the variables `NUM_MSEC_CROSS`, `NUM_MSEC_IMAGE`, `NUM_MSEC_SENTINEL`, and `NUM_MSEC_CHAR` to change how long the fixation cross, target images, sentinel images, and codecharts are shown to the participant. Adjust any other variables in the "UI Parameters" section that you desire.
3. Edit the file `config.json` to customize the task title, instructions, and disclaimer. You can also set the boolean `advanced.includeDemographicSurvey` to include a demographic survey at the end of the task, and you can set `advanced.hideIfNotAccepted` to block continuing with the task if it is on MTurk and the worker has not accepted the task. 
4. Decide how you want to store the collected task data. 
  * **Option 1: use MTurk.** This code base works out-of-the-box as an MTurk `ExternalQuestion`. Post this repository with your generated task data to a public url and point your MTurk task to that url. (For an example of how to launch a HIT on MTurk, see [this example MTurk notebook](https://github.com/a-newman/mturk-template/blob/master/mturk/mturk.ipynb).)
  * **Option 2: set up your own data storage.** You can configure the interface to post the collected data to an API endpoint of your choice. The API should save the posted data and return a unique key that can be used to identify the data submitted. More specifically, the url should save JSON data submitted via a `POST` request and return a JSON response of the form `{"key": <submission_code>}`. The submission code will be displayed to the user as proof of task completion (for instance, so that the user can enter the submission code back to an MTurk task). 
  * Alternatively, the [`print_data`](https://github.com/turkeyes/codecharts/tree/print_data) branch of this repository contains a version that downloads the data directly to a local file. You can use this to test your task before launching it with a back-end, or you can use this as-is to collect data with local participants.

## Table of Contents

* `config.json`: configuration files containing general task-setup parameters. 
* `index.html`: main html file for the interface 
* `assets/`: contains JavaScript files and input data for the interface as well as some additional libraries and assets. Important files detailed below: 
    * `js/custom.js`: JS file containing all task-specific logic. Most changes you make to the interface should involve this file. 
    * `js/main.js`: generic file handling task flow, data submission, etc. Does not contain task-specific logic. 
    * `task_data`: default folder for storing task input data.
* `generate-experiment-files/`: contains Python code for generating the data required to run the experiment (including the codecharts themselves) 
    * `main.ipynb`: a Jupyter notebook that walks you through the steps of generating the task data. 
