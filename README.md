# Meraki_Template_MG_Check

This script runs the following logic - 
grabs all networks with specific Tag
	⁃	For each tagged networks,
	⁃	identify what Template it belongs to and store that
	⁃	store networks name
	⁃	split the network (retain the new split networks)
	⁃	check if one of the new split networks is an MG network
	⁃	if not, create a new MG network, bind to the same template as original network and combine with the previously split networks with the original networks name. 
	⁃	if yes, recombine split networks with original networks name.
	⁃	Move onto the next network 

To run this script -
1. Download dependencies from requirements.txt
3. add your Meraki API key under .env file
4. run main.py
5. follow the prompt to enter number by the organization you want to run this script on
6. enter the name of the network tag you would like to run this script against.
