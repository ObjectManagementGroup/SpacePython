## SpacePython Examples

Example SpacePython example procedure scripts and an example implementation backing are included in the test directory.

Test procedures include:
  - ConfigureFEP.py
  - PassSetup.py
  - SetMomentumWheelSpeed.py

A configuration yaml file is included in the data sub-directory.

An example implementation backing is provided in the data sub-directory.

The demo requires the pyyaml module, which can be installed via the following command:

```
python3 -m pip install pyyaml
```

Once the space module has been installed, run the samples with the following example usage:

```
SPACEPYTHON_DEFAULT_MODULE=demo.DemoSpacePython python3 ConfigureFEP.py
```

This example demonstrates specifying a default module of demo.DemoSpacePython, which is the example implementation backing included.