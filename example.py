#!/usr/bin/env python3

import boto3, prettytable, argparse

parser = argparse.ArgumentParser(description='AWS Query Example.')
parser.add_argument('-t', '--tag', action='append', required=True, help='tag')
parser.add_argument('-r', '--regions', required=True, help='comma separated AWS regions')
args = parser.parse_args()

service = 'ec2'
regions = args.regions.split(',')
tag = args.tag

clients = list()

for region in regions:
    clients.append(boto3.resource(service, region))

for i in range(len(clients)):
    clients[i] = clients[i].instances.all()

table = prettytable.PrettyTable(['Region','Name','IP'])
for i in range(len(clients)):
    for instance in clients[i]:
        if instance.private_ip_address is None or instance.state['Name'] != 'running':
            break
        idx = [ i for i, tag in enumerate(instance.tags) if tag['Key'] == 'Name' ]
        #f = lambda enumerated: i for i, tag in enumerated if tag['key'] == 'Name'
        #idx = list(filter(f , enumerate(instance.tags)))
        if idx:
            if tag[0] in instance.tags[idx[0]]['Value']:
                table.add_row([regions[i],instance.tags[idx[0]]['Value'],instance.private_ip_address])
        else:
            continue

print(table)
