# UCTT

The Universal Cluster Testing Toolbox

## Design

UCTT leverages configerus configuration to configure a number of plugins that
are used to manage a cluster.
The toolbox helps you get a cluster started and accessible, and then lets you
tear it all down.

## UCTT plugins

UCTT is heavily plugins based.  Plugins are registered in UCTT by registering
them using UCTT decoration on plugin factory functions.  If you import a file
that has the decoration, then the plugin is registered and can be used.

We even leverage configerus bootstrapping to import files that include the
factory decoration.

## Tools

## Configerus

We rely heavily on dymanic and abstract configuration using configerus. Most of
the components come with out of the box defaults that work well as long as you
have good config in place.

Determing how to use the toolbox often comes down to discovering the convention
for the tools, and the convetions for the plugins that you want to use.

### Provisioners

The toolbox provides a number of dummy and contrib provisioner implementations
for starting, stopping and connecting to a cluster.

### Clients

Client plugins provide mechanisms for interacting with a cluster.  Clusters are
pretty diverse in behaviour as they are designed to allow interaction with very
specific APIS.

Clients are usually produced directly by a provisioner, as it is aware of what
clients it can be produces.

Clients can be used directly, or as a part of a workload.

Often the goal for a client is to allow common SDK/API access for common systems
such as a docker daemon, a kubernetes cluster or helm.  To do this most clients
try to directly extend common python distributions/packages.

### Workloads

Workload plugins let you apply a workload to a cluster using clients, which are
usually pulled directly from a provisioner.

## Integration

The toolbox is designed to be used in parts, with either contrib or custom code
as needed.

Parts can be used with any testing framework or cli tool.  Parts are designed to
be somewhat thread safe, and only conflict in parrallel where unavoidable.

## Usage

As we heavily rely on configerus to configure elements, you first need to create
usable configerus.config.Config objects.

Typical worklow is to pass a Config object directly to UCTT to ask for a
provisioner. The provisioner is then used to manage the cluster, and provide
clients.  Workloads allow us to standardize loads to apply using clients from
a provisoner.

Workflow:

1. build a configerus Config object on your own.
    Make sure that you have have config sources which will meet the needs of the
    provisioner and workloads that you want.
2. pass the Config object to uctt to ask for a Provisioner based on the config
3. use the Provisioner to start a cluster for testing

4. test your cluster:
    - ask the provisioner plugin for clients to access the cluster
    - use workloads to apply load to a cluster

5. use the provisioner plugin to destroy any resources that you created.
