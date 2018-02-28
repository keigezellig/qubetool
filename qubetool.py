import argparse

import subprocess


def constructArgParser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='subcommands', description='Valid subcommands are:', dest="command")
    project_parser = subparsers.add_parser(name='project', help='Activates a google cloud project')
    project_parser.add_argument('projectname', help='The name of the google cloud project')

    cluster_parser = subparsers.add_parser(name='cluster', help='Cluster commands')
    cluster_subparsers = cluster_parser.add_subparsers(title='Cluster commands', description='Valid commands are:',
                                                       dest='cluster_command')

    create_clusterparser = cluster_subparsers.add_parser(name='c',
                                                         description='Creates a kubernetes cluster in the current google cloud project',
                                                         help='Creates a kubernetes cluster in the current google cloud project')
    create_clusterparser.add_argument('clustername', help='Cluster name')
    create_clusterparser.add_argument('--zone', help='Google compute zone in which this cluster should run',
                                      default='europe-west1-c')

    delete_clusterparser = cluster_subparsers.add_parser(name='d',
                                                         description='Deletes a kubernetes cluster in the current google cloud project',
                                                         help='Deletes a kubernetes cluster in the current google cloud project')
    delete_clusterparser.add_argument('clustername', help='Cluster name')

    start_clusterparser = cluster_subparsers.add_parser(name='start',
                                                        description='Starts a kubernetes cluster in the current google cloud project',
                                                        help='Starts a kubernetes cluster in the current google cloud project')
    start_clusterparser.add_argument('clustername', help='Cluster name')

    stop_clusterparser = cluster_subparsers.add_parser(name='stop',
                                                       description='Stops a kubernetes cluster in the current google cloud project',
                                                       help='Stops a kubernetes cluster in the current google cloud project')
    stop_clusterparser.add_argument('clustername', help='Cluster name')

    switch_clusterparser = cluster_subparsers.add_parser(name='sw',
                                                         description='Switches to another kubernetes cluster in the current google cloud project',
                                                         help='Switches to another kubernetes cluster in the current google cloud project')
    switch_clusterparser.add_argument('clustername', help='Cluster name')

    cluster_subparsers.add_parser(name='i', description='Returns ip address of active cluster',
                                  help='Returns ip address of active cluster')
    cluster_subparsers.add_parser(name='n', description='Returns name of active cluster',
                                  help='Returns name of active cluster')
    cluster_subparsers.add_parser(name='comp', description='Returns components of active cluster',
                                  help='Returns components of active cluster')
    cluster_subparsers.add_parser(name='l', description='Returns list of all exitsing clusters in the project',
                                  help='Returns list of all exitsing clusters in the project')

    pod_parser = subparsers.add_parser(name='pod', help='Pod commands')
    pod_subparsers = pod_parser.add_subparsers(title='Pod commands', description='Valid commands are:',
                                               dest='pod_command')

    tail_podparser = pod_subparsers.add_parser(name='t', description='Shows log of a pod', help='Shows log of a pod')
    tail_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    attach_podparser = pod_subparsers.add_parser(name='a', description='Attaches to a pod', help='Attaches to a pod')
    attach_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    exec_podparser = pod_subparsers.add_parser(name='e', description='Executes command in the pod',
                                               help='Executes command in the pod')
    exec_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    restart_podparser = pod_subparsers.add_parser(name='r', description='Restarts a pod', help='Restarts a pod')
    restart_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    version_podparser = pod_subparsers.add_parser(name='v',
                                                  description='Shows the version of the docker container in the pod',
                                                  help='Shows the version of the docker container in the pod')
    version_podparser.add_argument('pod expression', help='A name or part of name (grep is used) of the pod')

    return parser


def run_command(command_with_args):
    command_parts = command_with_args.split()
    try:
        output = subprocess.run(command_parts, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=True)
        print("Command executed succesful")
        result = {"result": "OK", "stdout": output.stdout.decode('UTF-8'), "stderr": output.stderr.decode('UTF-8')}
        print(result)
        return result
    except subprocess.CalledProcessError as e:
        print("Command executed with errors")
        result = {"result": "ERROR", "stdout": e.stdout.decode('UTF-8'), "stderr": e.stderr.decode('UTF-8')}
        print(result)
        return result


def switch_project(projectname):
    cmd = 'gcloud config set project {projectname}'.format(projectname=projectname)
    run_command(command_with_args=cmd)


def create_cluster(clustername, zone, namespace):
    print('Set zone to {zone}'.format(zone=zone))
    set_zone_cmd = run_command("gcloud config set compute/zone {zone}".format(zone=zone))
    if set_zone_cmd['result'] == 'ERROR':
        return

    print('Create cluster {cluster}'.format(cluster=clustername))
    create_cluster_cmd = run_command('gcloud container clusters create {clustername} --machine-type n1-standard-1\
                 --image-type GCI\
                 --disk-size 10\
                 --scopes https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
                 --num-nodes 1\
                 --enable-cloud-logging\
                 --no-enable-cloud-monitoring'.format(clustername=clustername))

    if create_cluster_cmd['result'] == 'ERROR':
        return

    print('Set context')
    set_context_cmd = run_command(
        'gcloud container clusters get-credentials {clustername}'.format(clustername=clustername))

    if set_context_cmd['result'] == 'ERROR':
        return

    print('Deploy dashboard')
    run_command(
        'kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml')


def handle_cluster_cmd(args):
    if args.cluster_command == 'c':
        create_cluster(clustername=args.clustername, zone=args.zone)

if __name__ == "__main__":
    argParser = constructArgParser()
    args = argParser.parse_args()

    if args.command == 'project':
        switch_project(projectname=args.projectname)

    if args.command == 'cluster':
        handle_cluster_cmd(args=args)



# project switch: gcloud config set project [PROJECT_ID]
# create cluster: gcloud config set compute/zone [ZONE]
#                 gcloud container clusters create [clustername] --machine-type "n1-standard-1"\
#                 --image-type "GCI"\
#                 --disk-size "100"\
#                 --scopes "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"\
#                 --num-nodes "1"\
#                 --enable-cloud-logging\
#                 --no-enable-cloud-monitoring
#                 gcloud container clusters get-credentials clustername
#                 kubectl create namespace NAMESPACENAME
#                 kubectl config set-context $(kubectl config current-context) --namespace=<insert-namespace-name-here>

# delete cluster:

# echo "Deleting cluster $CLUSTER_NAME"
# 	gcloud container\
# 	 --project "$PROJECT_NAME"\
# 	 clusters delete "$CLUSTER_NAME"\
# 	 --zone "$CLUSTER_ZONE"
#
# 	echo "Deleting disks $CLUSTER_NAME"
# 	DISKS=`gcloud compute disks list | grep -i "$CLUSTER_NAME" | awk '{print $1}'`
# 	for DISK in $DISKS;
# 	do
# 		echo "Deleting $DISK"
# 		gcloud compute disks delete "$DISK"
# 	done
#
