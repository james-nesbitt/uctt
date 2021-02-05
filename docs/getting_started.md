# Getting Started

## Getting it installed.

```
pip install uctt
```

## Use UCTT in python code

With UCTT installed, you now need to write an application which imports it.

You are going to want to start by creating a Config object and using that to get
a provisioner object

```
# Import configerus for config generation
import configerus
from configerus.contrib.path PLUGIN_ID_CONFIGSOURCE_PATH
from configerus.contrib.dict PLUGIN_ID_CONFIGSOURCE_DICT

# Import the uctt core
import uctt
# Maybe we'll ask for a docker client later
import uctt.contrib.docker as uctt_docker

# we will use these as well
import datetime
import getpass

# New config
config = configerus.new_config()
# Add ./config path as a config source
config.add_source(PLUGIN_ID_CONFIGSOURCE_PATH, 'project_config').set_path(os.path.join(__dir__, 'config'))
# Add some dymanic values for config
config.add_source(PLUGIN_ID_CONFIGSOURCE_DICT, 'project_dynamic').set_data({
    "user": {
        "id": getpass.getuser() # override user id with a host value
    },
    "global": {
        "datetime": datetime.now(), # use a single datetime across all checks
    },
    config.paths_label(): { # special config label for file paths, usually just 'paths'
        "project": __DIR__  # you can use 'paths:project' in config to substitute this path
    }
})

# provisoner from config
prov = uctt.new_provisioner_from_config(config, 'my_provisioner')
```

That code will read a whole bunch of config.

To get a provisioner, you are going to need at least the following config:

'provisioner.yml':
```
plugin_id: {what backend plugin do you want to use}
```
(check what else your particular provisioner expects)

## What can I do with it

Use it to start up cluster resources

```
prov.prepare()
prov.apply()

prov.get_client(mtt_docker.UCTT_PLUGIN_ID_DOCKER_CLIENT)

# do some docker stuff
ps = docker_client.containers.list()
```

And lot's more.

Don't forget to tear it all down.

```
prov.destroy()
```

## What more

take a look at the `./demos`.  You can find some examples there of some very
simple feature elements, and also some full featured testing demos
