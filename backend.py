from http.client import responses

import meraki
import os
from dotenv import load_dotenv
import json

# load all environment variables
load_dotenv()


def get_orgs():
    """Gets the list of all orgs (name and id) that admin has access to"""
    orgs = []
    dict = {"id": "", "name": ""}
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizations()

    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        orgs.append(dict)
        dict = {"id": "", "name": ""}

    return orgs


def get_networks(org_id):
    """Get a list of networks and returns dict with net IDs and names"""
    nets = []
    dict = {"id": "", "name": ""}
    # collect network names
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizationNetworks(
        org_id, total_pages='all'
    )
    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        nets.append(dict)
        dict = {"id": "", "name": ""}

    return nets

def get_networks_by_tag(org_id, tag):
    """Get a list of networks and returns dict with net IDs and names"""
    nets = []
    dict = {"id": "", "name": ""}
    # collect network names
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizationNetworks(
        org_id, total_pages='all'
    )
    for i in response:
        if tag in i["tags"]:
            dict["id"] = i["id"]
            dict["name"] = i["name"]
            nets.append(dict)
            dict = {"id": "", "name": ""}

    return nets

def isNetworkTemplateBound(net_id):
    """Check if a network is bound to a template"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.getNetwork(net_id)
    print(response)
    if response["isBoundToConfigTemplate"] == True:
        return True
    else:
        return False

def getTemplateID(net_id):
    """Get the template ID of a network"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.getNetwork(net_id)
    template_id = response["configTemplateId"]
    return template_id

def getTemplateName(template_id, org_id):
    """Get the template name of a network"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizationConfigTemplate(org_id, template_id)
    return response["name"]

def getNetworkName(net_id):
    """Get the name of a network"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.getNetwork(net_id)
    return response["name"]

def networkSplit(net_id):
    """Split a network into two networks"""
    splitNetworks = []
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.splitNetwork(net_id)
    for i in response['resultingNetworks']:
        splitNetworks.append(i['id'])
    return splitNetworks

def checkforMG(nets):
    """Check if a list of network IDs has an MG, returns True if it does"""
    listOfNetworks = []
    for network_id in nets:
        dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
        response = dashboard.networks.getNetwork(network_id)
        listOfNetworks.append(response)
    for i in listOfNetworks:
        for i in i['productTypes']:
            if i == "cellularGateway":
                return True

def createMGnetwork(org_id):
    """Create an MG network and returns its network ID"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.createOrganizationNetwork(org_id, name="MG Network", productTypes=["cellularGateway"])
    print(f"MG Network created {response["id"]}")
    return response["id"]

def networkCombine(org_id, nets, name):
    """Combine multiple networks. Takes a list of network IDs as input"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.combineOrganizationNetworks(org_id, name, nets)
    print(response)

def bindMGtoTemplate(net_id, template_id):
    """Bind an MG network to a template"""
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.bindNetwork(net_id, template_id, autoBind=False)
    print(response)


