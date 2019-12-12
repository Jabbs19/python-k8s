# python-k8s
Python K8s Client Watcher

Installation

Python 2.7 or 3.4+
Create a venv
Install kubernetes client

From source:

git clone --recursive https://github.com/kubernetes-client/python.git
cd python
python setup.py install

From PyPi directly:

pip install kubernetes


To Run:

python3 watchPullEvents.py


Other:

- Still in pseudo-code in some cases
- Manifest to BQ Field Mappings configurable
- Sees all events, but only takes action on PULLED
- Ultimately, we should just filter out other events (i.e. REASONs)

