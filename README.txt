===========
SpacePython
===========

The space package defines SpacePython, a high level interface to a Spacecraft
Operations Center for spacecraft monitoring and control.  The scripts included
in the package exercise the normative interfaces for SpacePython and should be 
runnable by any SpacePython-compliant implementation.  

Each function and class definition in a space module that is required for a 
SpacePython implementation is imported by the space package __init__.py file, 
and is also marked in the module with the comment "#Normative".  If a class is 
normative, then all of its methods are normative, unless they are explicitly
marked non-normative.  There are helper classes and module variables that are 
part of the skeleton implementation, but are not marked #Normative and are
not required in a compliant implementation.

The included dataset, SpacePythonDataset.yaml, 
provides command, directive, and parameter lists to
allow running the procedures in the skeleton, but should be replaced with 
the database definition formats used by the Spacecraft Operations Center 
software.  The yaml format is not a required input format, but is provided 
only to allow running the example scripts.  SpacePythonDataset.yaml should 
be copied to the user's home directory for the example package loader to find 
it.  

=============================
