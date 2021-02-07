"""

MTT Terraform

MTT contrib functionality for terraform.  Primarily a terraform provisioner
plugin.

"""

from configerus.config import Config

from uctt import plugin as uctt_plugin

from .provisioner import TerraformProvisionerPlugin

UCTT_TERRAFORM_PROVISIONER_PLUGIN_ID = 'uctt_terraform'
""" Terraform provisioner plugin id """


@uctt_plugin.Factory(type=uctt_plugin.Type.PROVISIONER,
                     plugin_id=UCTT_TERRAFORM_PROVISIONER_PLUGIN_ID)
def uctt_plugin_factory_provisioner_terraform(
        config: Config, instance_id: str = ""):
    """ create an mtt provisionersss dict plugin """
    return TerraformProvisionerPlugin(config, instance_id)


""" SetupTools EntryPoint BootStrapping """


def bootstrap(config: Config):
    """ UCTT_Terraform bootstrap

    We dont't take any action.  Our purpose is to run the above factory
    decorator to register our plugin.

    """
    pass
