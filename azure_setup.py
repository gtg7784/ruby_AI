import azureml.core
from azureml.core import Workspace

print(azureml.core.VERSION)

subscription_id = 'd294ecf5-c9bb-49ce-8ad5-9707f6504612'
resource_group  = 'ruby_resource'
workspace_name  = 'ruby_workspace'

try:
    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    ws.write_config()
    print('Library configuration succeeded')
except:
    print('Workspace not found')