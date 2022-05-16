# Usability Eye tracking
This application can be used for generating heatmaps based on eye movements, in the context of conducting usability tests.
## Contributing
Contributions can be sent via PRs. They will be reviewed, and if deemed useful, merged with the existing code base.

## Installation
1. Clone this repository
2. Create an environment (we recommend anaconda/miniconda)
3. Run `conda install -c conda-forge dlib` (or whichever method the env prefers for getting dlib)
4. Run `pip install -r requirements.txt` from project directory

## Usage
To run the code, be in the project directory and run `python src/controller.py`.

## Code Coverage
To generate a coverage report, start by installing `coverage` and `pytest` with `pip install coverage pytest`.
1. run `coverage run -m pytest`
2. run `coverage html --omit="tests/*,config*,*__init__.*"` (or coverage report, for more information: [view documentation](https://coverage.readthedocs.io/en/6.3.3/)
