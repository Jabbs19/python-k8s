# python-k8s
Python K8s Client Watcher

## **Requirements**
Python 2.7 or 3.4+

## **Installation** 

Create a venv 

### Install kubernetes client

#### From source:

`git clone --recursive https://github.com/kubernetes-client/python.git`
`cd python`
`python setup.py install`

#### From PyPi directly:

`pip install kubernetes`


## Running
`python3 watchPullEvents.py`

## To Do:
- Credentials and kubeconfig may need some additional work.  Using gcloud is easy, but need to inject in.  Maybe as part of config.ini passed to python.  I get some credentials errors occasionally, but I think its just gcloud creds expiring in my testing.


## Other:

- Still in pseudo-code in some cases
- Manifest to BQ Field Mappings configurable
- Sees all events, but only takes action on PULLED
- Ultimately, we should just filter out other events (i.e. REASONs)

