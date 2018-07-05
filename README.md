# SAXS&SANS -Profile Computation- 

version 1.0 25/06/2018.

SAXS&SANS -Profile Computation- is a web application made with [Dash](https://dash.plot.ly/) which is a Python framework. This application permits to :
* Predict or fit the X-Ray or neutrons small-angle scattering profile calculation
* Select various parameters to simulate at best the experiment
* Display the result in a graph and provide download links to save the results

thanks to the [Pepsi-SAXS](https://team.inria.fr/nano-d/software/pepsi-saxs/) and [Pepsi-SANS](https://team.inria.fr/nano-d/software/pepsi-sans/) softwares.

### Prerequisites 

In your terminal, install several dash libraries. These libraries are under active development, so install and upgrade frequently.

```
pip install dash==0.21.1  # The core dash backend
pip install dash-renderer==0.13.0  # The dash front-end
pip install dash-html-components==0.11.0  # HTML components
pip install dash-core-components==0.23.0  # Supercharged components
pip install plotly --upgrade
```

Install Flask 

```
pip install Flask
```
Python 3 is supported.

In the bin folder, put the [Pepsi-SAXS](https://team.inria.fr/nano-d/software/pepsi-saxs/) and [Pepsi-SANS](https://team.inria.fr/nano-d/software/pepsi-sans/) softwares which you have to download first.

## Running 

```
python3 app.py
```

## Versioning

Python 3.6.5
Flask 1.0.2

## Authors

**Marion GASSER**

See also the list of contributors : 
* Sergei Grudinin
* Anne Martel
* Jamie Hall

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
