# Circulation

Circulation encourages people to re-use resources which are too often single use. How many of the books in your home will only be read by one person when there is no reason they could not be read by many people? By making our personal resources available to our neighbors, we hope to foster exchanges in our communities.

## Key Features
* Support for multiple languages
* Mobile responsive

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [Python](https://www.python.org/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

### Installing
```sh
git clone https://github.com/justincredble/circulation.git

cd circulation

virtualenv ./venv

source ./venv/bin/activate

pip install -r requirements.txt

python ./run.py
```

or with Pipenv
```bash
pipenv install
pipenv run python run.py
```

## Built With

* [Flask](http://flask.pocoo.org/) - Python Web framework
* [SQLite](https://www.sqlite.org/) - Database
* [Bootstrap](http://getbootstrap.com/) - CSS framework

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/justincredble/circulation/tags).

## Authors

* **阿卡琳** - *Initial work* - [hufan-akari](https://github.com/hufan-akari)
* **Justin McLemore** - [justincredble](https://github.com/justincredble/)
* **Philip Diller** - [PhilipDiller](https://github.com/PhilipDiller)

See also the list of [contributors](https://github.com/justincredble/circulation/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
