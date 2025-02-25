import backend
from backend import isNetworkTemplateBound

def main():
    """runs the program and repeats unless user cancels the prompt"""
    flag = True
    while flag:
        orgs = backend.get_orgs()
        x = 1
        y = 1
        z = 1
        for i in orgs:
            print(f"{x}. {i['name']}")
            x = x + 1
        org_num = int(input("Select an organization by its number: "))
        org = orgs[org_num - 1]
        org_id = org['id']

        tagInput = input("Enter the tag you would like to pull networks for: ")
        taggedNetworks = backend.get_networks_by_tag(org_id, tagInput)
        for i in taggedNetworks:
            print(f"{z}. {i['name']}")
            z = z + 1
        continueScript = input("Would you like to continue with the list of these network? Y to continue N to exit: ")
        if continueScript.lower() == 'y':
            # identify what Template it belongs to and store that
            for network in taggedNetworks:
                if isNetworkTemplateBound(network['id']):
                    templateID = backend.getTemplateID(network['id'])
                    print(f"{network['name']} is bound to a template + {templateID}")
                    print(f"Splitting {network['name']}...")
                    split_Networks = backend.networkSplit(network['id'])
                    print(f"Splitting {network['name']} complete")
                    print(f"Checking if one of the new split networks is an MG network...")
                    if backend.checkforMG(split_Networks):
                        print("An MG network was found")
                        print("Recombining split networks with original network name...")
                        backend.networkCombine(org_id, split_Networks, network['name'])
                        print("Recombining complete")
                    else:
                        print("An MG network was not found")
                        print("Creating a new MG network...")
                        new_MG = backend.createMGnetwork(org_id)
                        print("New MG network created")
                        print("Binding MG network to the same template as the original network...")
                        backend.bindMGtoTemplate(new_MG, templateID)
                        print("Binding complete")
                        print(f"Adding {new_MG} to split networks")
                        split_Networks.append(new_MG)
                        print("Combining split networks with original network name...")
                        backend.networkCombine(org_id, split_Networks, network['name'])
                        print("Combining complete")

                else:
                    print(f"{network['name']} is not bound to a template")

        else:
            break

        repeat = input("Would you like to run the script again? Y to continue N to exit: ")
        if repeat.lower() == 'y':
            flag = True
        else:
            flag = False


if __name__ == '__main__':
    main()