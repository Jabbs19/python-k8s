from kubernetes import client, config, watch
from . import watcher

def main():
 
  config.load_kube_config()

  #listPullEvents()
  #listImagesInAllCurrentPods()
  watcher.watchPullEvents()

if __name__ == '__main__':
    main()