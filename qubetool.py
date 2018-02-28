import argparse


def constructArgParser():
    parser = argparse.ArgumentParser()


    subparsers = parser.add_subparsers(title='subcommands', description='Valid subcommands are:', dest="command")
    project_parser = subparsers.add_parser(name='project', help='Activates a google cloud project')
    project_parser.add_argument('projectname', help='The name of the google cloud project')


    cluster_parser = subparsers.add_parser(name='cluster',  help='Cluster commands')
    cluster_subparsers = cluster_parser.add_subparsers(title='Cluster commands', description='Valid commands are:', dest='cluster_command')

    create_clusterparser = cluster_subparsers.add_parser(name='c', description='Creates a kubernetes cluster in the current google cloud project', help='Creates a kubernetes cluster in the current google cloud project')
    create_clusterparser.add_argument('clustername', help='Cluster name')
    create_clusterparser.add_argument('--zone', help='Google compute zone in which this cluster should run', default='europe-west1-c')


    delete_clusterparser = cluster_subparsers.add_parser(name='d',description='Deletes a kubernetes cluster in the current google cloud project', help='Deletes a kubernetes cluster in the current google cloud project')
    delete_clusterparser.add_argument('clustername', help='Cluster name')

    start_clusterparser = cluster_subparsers.add_parser(name='start',description='Starts a kubernetes cluster in the current google cloud project', help='Starts a kubernetes cluster in the current google cloud project')
    start_clusterparser.add_argument('clustername', help='Cluster name')

    stop_clusterparser = cluster_subparsers.add_parser(name='stop',description='Stops a kubernetes cluster in the current google cloud project', help='Stops a kubernetes cluster in the current google cloud project')
    stop_clusterparser.add_argument('clustername', help='Cluster name')

    switch_clusterparser = cluster_subparsers.add_parser(name='sw',description='Switches to another kubernetes cluster in the current google cloud project', help='Switches to another kubernetes cluster in the current google cloud project')
    switch_clusterparser.add_argument('clustername', help='Cluster name')

    cluster_subparsers.add_parser(name='i',description='Returns ip address of active cluster', help='Returns ip address of active cluster')
    cluster_subparsers.add_parser(name='n',description='Returns name of active cluster', help='Returns name of active cluster')
    cluster_subparsers.add_parser(name='comp',description='Returns components of active cluster', help='Returns components of active cluster')
    cluster_subparsers.add_parser(name='l',description='Returns list of all exitsing clusters in the project', help='Returns list of all exitsing clusters in the project')


    pod_parser = subparsers.add_parser(name='pod',  help='Pod commands')
    pod_subparsers = pod_parser.add_subparsers(title='Pod commands', description='Valid commands are:', dest='pod_command')

    tail_podparser = pod_subparsers.add_parser(name='t', description='Shows log of a pod', help='Shows log of a pod')
    tail_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    attach_podparser = pod_subparsers.add_parser(name='a', description='Attaches to a pod', help='Attaches to a pod')
    attach_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    exec_podparser = pod_subparsers.add_parser(name='e', description='Executes command in the pod', help='Executes command in the pod')
    exec_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    restart_podparser = pod_subparsers.add_parser(name='r', description='Restarts a pod', help='Restarts a pod')
    restart_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    version_podparser = pod_subparsers.add_parser(name='v', description='Shows the version of the docker container in the pod', help='Shows the version of the docker container in the pod')
    version_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')






    return parser


if __name__ == "__main__":
    argParser = constructArgParser()
    args = argParser.parse_args()
    print(args)
