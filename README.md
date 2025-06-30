# SpacePython

Managed by the Object Management Group

Project Website: https://www.omg.org/solm/

## Package Description

The space package defines SpacePython, a high level interface to a Spacecraft
Operations Center for spacecraft monitoring and control.  The scripts included
in the test directory package exercise the normative interfaces for SpacePython 
and should be runnable by any SpacePython-compliant implementation with a 
similar operating configuration.  

Each function and class definition in a space module that is required for a 
SpacePython implementation is marked as an abstract class or function.

Within the test directory, the included dataset, SpacePythonDataset.yaml, 
provides command, directive, and parameter lists to allow running the 
example procedures, but should be replaced with 
the database definition formats used by the Spacecraft Operations Center 
software.  The yaml format (and the pyyaml module) is not a required input 
format, but is required for running the example scripts.

## Package Build Instructions

First, make sure that you have latest pip installed

```
python3 -m pip install --upgrade pip
```

Second, install the build tooling

```
python3 -m pip install --upgrade build
```

Lastly, perform a build

```
python3 -m build
```

## Reporting Issues
If you have issues, please share them with the Object Management Group via our issue tracker at https://issues.omg.org/