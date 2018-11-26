[![Documentation Status](https://readthedocs.org/projects/vitaflow/badge/?version=latest)](https://vitaflow.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/imaginea/vitaflow/blob/master/LICENSE)
 

# vitaFlow - VideoImageTextAudioFlow
 ![](vitaflow-icon.png)
 
## Introduction

Deep Learning projects are increasing exponentially in recent times and the complexity 
of handling such projects alike across the domains. 
Be it business environment or in any online competitions, the main challenge is  
how we can reuse the code base what we have developed for one requirement/problem 
statement and use it to a slightly different new requirement/problem statement. 
We are incubating a ideation to solve this typical software design problem for 
Deep Learning projects, which would simplify the whole process of data preparation, 
modelling and serving in a easy configurable plug and play framework.

## Problem Statement

To come up with a framework that enables a fast prototyping of Deep Learning 
models that handles Video/Image/Text/Audio and provide an seamless way serving them
in different end points.

- **A Navie Developer** : Can I get an experimentation play ground, with some set of 
open datasets, data iterators and models? to learn by doing?
- **A Data Scientist** : Can I build a model with an avaiable open dataset and later switch 
to production dataset when the Data Engineering team bring in the production data?
- **A Data Engineer** : Can I use any available model and run through my data during my data preparation cycle?
- **Online Competitioner** : Can I reuse the models and pieces of modules that I have developed for my last competition 
in my current competition? 
- **Business Deadlines** : We had spend few months of effort while addressing a clients proposals and build a prototype.
Can we showcase the prototype developed to upcoming project proposals as quick as possible? 

In our Deep Learning exploration/projects we wanted to build a framework that is modular as much as possible, 
plug ang play architecture for main modules and reuse our experience (hours of development and testing) from one 
project to another, while improving on existing capabilities without breaking it.  
 
## Proposed Solution

**Data Science wisdom comes only through failed experimentation - Damian Mingle**

The thought process is to come up with following modular components which then can be then glued through
configuration:
 - Data Collection and Cleansing
 - Dataset modules with pre-processing modules
 - DataIterator modules (backed by [TF Data](https://www.tensorflow.org/guide/datasets))
 - Tensorflow Models (backed by [Estimators](https://www.tensorflow.org/guide/estimators))
 - A Engine to run the models
 - Tensorflow model serving using [TFLite](https://www.tensorflow.org/lite/)
    - Web app
    - Mobile

## Architecture

![](docs/images/vitaflow_stack.png)

## vitaFlow in Action

CoNLL 2003 data set is considered since the data size small and easy to test:

Run a experiment pointing to this [config](examples/conll2003/config.py),
which uses this [dataset](https://imaginea.github.io/vitaFlow/build/html/api/data/text/conll/conll_2003_dataset.html),
and this [data iterator](https://imaginea.github.io/vitaFlow/build/html/api/data/text/iterators/conll_csv_in_memory.html),
and this [model](https://imaginea.github.io/vitaFlow/build/html/api/models/text/seq2seq/bilstm_crf.html).

``` bash
cd /path/to/vitaflow/
python vitaflow/run/run.py --config_python_file=examples/conll2003/config.py
```

- The whole experimentation is configured from once place, based on the string names and corresponding config params
- The `experiment run engine` takes care of setting up the modules which includes but not limited to,
downloading the dataset, pre-processing the dataset, iterator initialization and finally running the model with check 
pointing the modle data as configured.

The big difference comes from the way the whole experiment can be configured. 
Say, if the model needs to replaced based on a latest paper published, it is simple as writing a model 
(that adheres some rules) and plugin into the vitaFlow, you are good to go with new model with old tested 
dataset and data iterator modules.

This level of configuration and project design will allows as to iterate the Deep Learning ideas as fast as possible to 
meet the business demands.

## Future Road Map

Add support for set of open datasets across domains and corresponding models based on published papers, tweak the model
to derive the best insights of given dataset, while exposing right sets of  configurations for any new incoming datasets.

With that in place, we hope it would reduce lot of efforts when we have to address any future requirements.

**As an example:**: 
We currently have Sequence to Sequence model(s) (text and character level embeddings) based on CoNLL dataset.
With that model and iterator in place, we can address any Seq2Seq model requirements, once we write a Dataset 
module for the new data that gives some predefined intermediate data for the data iterator.