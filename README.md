# elasticsearch-tests-behave
This is a repo written in python behave. The purpose is to test the functionality of elastic search components using a BDD testing framework. 

## Requirements

### Elastic Search

This repository requires an instance of elastic search to be up an running on a local host. See this [docker-elk repository](https://github.com/rysantos/docker-elk)

### Behave
[Behave Documentation](https://behave.readthedocs.io/en/latest/)
[Behave Repository](https://github.com/behave/behave/blob/master/docs/index.rst)

This repository requires behave to be installed
```console
$ pip install behave
```

## Usage

General behave usage is to change directory into the desired test suite then run the behave command

```console
$ cd ./Tests/elastticsearch_tests
$ behave
```
Sample Output
```console
0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 1 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 4 untested
Took 0m0.000s
```

### Elasticsearch Tests

Tests the functionality of elasticsearch by writting 10 entries to a test index and reading them back from said index

### Metricbeat Tests

Tests the metricbeat index for beat functionality and data integrity

### Heartbeat Tests

Tests the heartbeat index for beat functionality and data integrity

### Filebeat Tests

(Half Completed)
Tests the filebeat index for beat functionality and data integrity

### Packetbeat Tests

(Not Completed)