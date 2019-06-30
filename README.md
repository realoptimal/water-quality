# water-quality

## Description

This application demonstrates a Flask-SqlAlchemy based API.  The purpose of the API is to surface information about water quality by `scoring`it according to an overall measure of collective concentration as a function of individual contamanant concentration and factors of their relative health hazardnous contribution.

## Problem Statment

Los Angeles recently sampled water quality at various sites, and recorded the presence of contaminants. Here's an excerpt of the table:(from: http://file.lacounty.gov/bc/q3_2010/cms1_148456.pdf)

#### Sample table of Contaminants
##### (All chemical values are in mg/L)

| id | site                                      | chloroform | bromoform | bromodichloromethane | dibromichloromethane |
| ---| ----------------------------------------- | ---------- | --------- | -------------------- | -------------------- |
|  1 | LA Aquaduct Filteration Plant Effluent    |   .00104   | .00000    |  .00149              |  .00275              |
|  2 | North Hollywood Pump Station (well blend) |   .00291   | .00487    |  .00547              |  .0109               |
|  3 | Jensen Plant Effluent                     |   .00065   | .00856    |  .0013               |  .00428              |
|  4 | Weymouth Plant Effluent                   |   .00971   | .00317    |  .00931              |  .0116               |

These four chemical compounds are collectively regulated by the EPA as Trihalomethanes, and their collective concentration cannot exceed .080 mg/L (from http://water.epa.gov/drink/contaminants/index.cfm#List )

#### Contaminant Hazardous-ness / Relative Strength ("Danger")

Some Trihalomethanes are nastier than others, bromodichloromethane and bromoform are particularly bad. That is, water that has .060 mg/L of Bromoform is generally more dangerous than water that has .060 mg/L of Chloroform, though both are considered "safe enough".

We could build a better metric by adjusting the contribution of each component to the Trihalomethane limit based on it's relative "danger". Furthermore, consider we want to try several different combinations of weights (factors).

#### Sample table of Factor weights:

|  id   | chloroform_weight | bromoform_weight | bromodichloromethane_weight | dibromichloromethane_weight |
| ----- | ----------------- | ---------------- | --------------------------- | --------------------------- |
|   1   |   0.8             |      1.2         |       1.5                   |     0.7                     |
|   2   |   1.0             |      1.0         |       1.0                   |     1.0                     |
|   3   |   0.9             |      1.1         |       1.3                   |     0.6                     |
|   4   |   0.0             |      1.0         |       1.0                   |     1.7                     |

### Collective Concentration
In statistics, a factor is a single value representing a combination of several component values. We may gather several different variables, which semantically indicate a similar idea, and, to make analysis simpler, we can combine these several values into a single "factor" and disregard the constituents

The weights that we should use in our factor could be a complex question. Ultimately it depends on what we're modeling.  For example, let's say the city has the option of installing one of several different filtration units to remove a specific Triahlomethane (but the city can't afford all of the filters). We can use differently weighted factors to simulate each of these and do a cost / benefit analysis informing the city's decision on which filtration unit to purchase.  Let's say someone from the city has already computed various factors they want to analyze, and put them in a factor_weights table.

In our case, we'll use a linear combination of the nth factor weights to compute the samples nth factor.

## Application

### Installing & Running

NOTE: You must have a version of mysql installed (v8.5+).  You can install a recent version using brew (if on a mac) `brew install mysql`.  Also, the setup script relies on your mysql having a root user with no password.  Please modify accordingly for your given setup/environment

Clone the repo and run the setup:

```sh
$ git clone https://github.com/realoptimal/water-quality.git
$ cd water-quality
$ ./setup.sh
```

The setup script will create the `water_quality` database and a system (admin) user for the database.  It will then setup your python virtual environment.

Start the application:

```sh
flask run
```

That's it!!! The application exposes several RESTful endpoints which can be called using curl or postman.

### API 

The API defaults to running on localhost port 5000

- `GET /api/contaminant/<int:contaminant_id>` : Gets info about contaminant with given _contaminant_id_.

- `POST /api/contaminant` : add a new contaminant with json describing the contaminant.  Requires a contaminant name, description and default weight to use for new factor sets.  Returns _contaminant_id_ key for the created contaminant record.

```json
{
  "name": "terrible-compound-X",
  "description": "some text about how bad this one is",
  "default_strength": 1.1
}
```

- `GET /api/sample` : Gets water sample info for all samples in the database.

- `GET /api/sample/<int:sample_id>` : Gets water sample info for sample with given _sample_id_.  Optional boolean parameter `include_factors=[true/false]` to return sample-factor calculated values for all known factor sets.

- `POST /api/sample` : add a new sample with json describing the sample.  Requires a site name and list of contaminant keyed by their _contaminant_id_ and their associated concentration.  Returns the _sample_id_ of the created record on success or indicates if sample record with site name already exists.  Contaminants not listed will be assumed to have zero concentration.

```json
{
  "site": "Some new pumping station",
  "contaminant_concentrations": [
     {
       "contaminant_id": 4,
       "concentration": 0.01234
     },
     {
       "contaminant_id": 3,
       "concentration": 0.02345
     },
     {
       "contaminant_id": 8,
       "concentration": 0.05234
     }
  ]
}
```

- `DELETE /api/sample/<int:sample_id>` : deletes a sample with given _sample_id_.

- `GET /api/factor` : Get contaminant strengths for all factor weight sets in the database.

- `GET /api/factor/<int:factor_id>` : Get contaminant strengths for a given factor weight set with given _factor_id_.

- `GET /api/sample-factor/<int:sample_id>/<int:factor_id>` : Gets sample "score" or weighted concentration for a given sample and factor weight set.

- `POST /api/factor` : add a new factor (weight set) to use or include in sample evaluation.  Requires a factor description and list of contaminants keyed by their _contaminant_id_ and associated relative-strength (weight) in the factor.  Returns the created _factor_id_ of the factor record.

```json
{
  "description": "New filtration factor",
  "contaminant_strengths": [
     {
       "contaminant_id": 1,
       "strength": 1.1
     },
     {
       "contaminant_id": 2,
       "strength": 2.7
     },
     {
       "contaminant_id": 3,
       "strength": 0.9
     }
  ]
}
```

- `DELETE /api/factor/<int:factor_id>` : deletes a factor set with given _factor_id_.


### Models & Views

The model and views code make use of two python libraries to make working with sqlalchemy a bit more convenient, namely Flask-SQLAlchemy and Flask-RESTful.

```python
# suppose the sample we want has sample_id = 2
>>> import json
>>> from wq_app import db
>>> from wq_app.framework.models import *
>>> sample2 = Sample.query.get(2)
>>> print(json.dumps(sample2.to_hash(), sort_keys=False, indent=4))
{
    "id": 2,
    "site": "North Hollywood Pump Station (well blend)",
    "contaminant_concentrations": [
        {
            "contaminant_id": 1,
            "contaminant_name": "chloroform",
            "concentration": 0.00291
        },
        {
            "contaminant_id": 2,
            "contaminant_name": "bromoform",
            "concentration": 0.00487
        },
        {
            "contaminant_id": 3,
            "contaminant_name": "bromodichloromethane",
            "concentration": 0.00547
        },
        {
            "contaminant_id": 4,
            "contaminant_name": "dibromichloromethane",
            "concentration": 0.0109
        }
    ]
}
>>> print(json.dumps(sample2.to_hash(include_factors=True), sort_keys=False, indent=4))
{
    "id": 2,
    "site": "North Hollywood Pump Station (well blend)",
    "contaminant_concentrations": [
        {
            "contaminant_id": 1,
            "contaminant_name": "chloroform",
            "concentration": 0.00291
        },
        {
            "contaminant_id": 2,
            "contaminant_name": "bromoform",
            "concentration": 0.00487
        },
        {
            "contaminant_id": 3,
            "contaminant_name": "bromodichloromethane",
            "concentration": 0.00547
        },
        {
            "contaminant_id": 4,
            "contaminant_name": "dibromichloromethane",
            "concentration": 0.0109
        }
    ],
    "factors": [
        {
            "factor_id": 1,
            "description": "New filtration factor 1",
            "value": 0.024007
        }
    ]
}
```

    
