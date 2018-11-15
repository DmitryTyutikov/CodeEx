#!/usr/bin/env python2.7

import argparse
import report_vars as rv
from as_report_class import Peering_report

parser = argparse.ArgumentParser()
parser.add_argument("asn", help="AS number you want to get report for", type=int)
args = parser.parse_args()

asn = args.asn
myPeering = Peering_report(asn)

file_name = 'Peering_report_ASN{}{}.txt'.format(myPeering.asn, myPeering.time.replace(' ', '_'))
intro = rv.intro.format(asn = myPeering.asn, name = myPeering.name, aka = myPeering.aka, date = myPeering.time, site = myPeering.site)
exec_summary = rv.exec_summary.format(asn = myPeering.asn, name = myPeering.name, c_number = myPeering.country_count, regions = myPeering.region_count, ipv4_number = myPeering.ipv4_count, ipv6_number = myPeering.ipv6_count, ix_count = myPeering.ix_count, link_count = myPeering.link_count, agg_speed = myPeering.agg_speed)

print "Report is ready and was saved as {file} in script directory. This is the content of the report:\n".format(file = file_name)

big_data = ''
for region, country in myPeering.ix_dict.iteritems():
	reg_header = rv.reg_header.format(r_name = region, c_num = len(myPeering.peerings_per_region(region)), ix_num = myPeering.ix_count_per_region(region), speed = myPeering.speed_per_region(region))
	print reg_header
	big_data += reg_header
	for country, ix in country.iteritems():
		country_header = rv.country_header.format(c_name = country, asn = myPeering.asn, ix_number = myPeering.ix_count_per_country(country), speed = myPeering.speed_per_country(country))
		print country_header
		big_data += country_header
		for ix, ix_details in ix.iteritems():
			ix_header = rv.ix_header.format(name = ix_details['name'].encode('ascii', 'ignore'), link_num = len(ix_details['links']))
			print ix_header
			big_data += ix_header
			for link in ix_details['links']:
				link_details = rv.link_details.format(ipv4 = link['ipv4'], ipv6 = link['ipv6'], speed = link['speed'])
				print link_details
				big_data += link_details

rep_file = open(file_name, 'w')
rep_file.writelines(intro)
rep_file.writelines(exec_summary)
rep_file.writelines(big_data)
rep_file.close()