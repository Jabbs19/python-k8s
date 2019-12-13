# python-k8s
Python K8s Client Watcher

Has a few different functions in there right now.  A watcher, which will watch for image pull events.  A similar funtioning one that will just list all, but I believe that "watch" actually scoops up history too (up to hour?).

Also has a listImagesInAllCurrentPods(), which will get multiple containers in a pod, and get the date they were "running" even if thats no longer stored in API resources.  Right now, just change the function in main() to change what it does.

## **Installation** 

Here is the link to the Python K8s install process:
[K8s Python Client Install](https://github.com/kubernetes-client/python#kubernetes-python-client "K8s Python Client Install")

### **Requirements**
Python 2.7 or 3.4+


### Process

Create a venv 

#### Install kubernetes client

##### From source:

`git clone --recursive https://github.com/kubernetes-client/python.git`
`cd python`
`python setup.py install`

##### From PyPi directly:

`pip install kubernetes`


## **Running**
`python3 watchPullEvents.py`

Uncomment 1 of the 3 functions in the main() function to either listImagePullEvents, getAllImagesInCurrentPods or watchImagePullEvents.

## To Do/Other:
- Credentials and kubeconfig may need some additional work.  Using gcloud is easy, but need to inject in.  Maybe as part of config.ini passed to python.  I get some credentials errors occasionally, but I think its just gcloud creds expiring in my testing.
- Still in pseudo-code in some cases
- Manifest to BQ Field Mappings configurable
- Sees all events, but only takes action on PULLED
- Ultimately, we should just filter out other events (i.e. REASONs)

