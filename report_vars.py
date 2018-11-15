#!/usr/bin/env python2.7

intro = '''AS Number: {asn}
Organization name:  {name}
Other known aliases: {aka}
Date of the report: {date}
Web site: {site}\n
'''

exec_summary = '''SUMMARY:
AS{asn}, owned by {name}, is present in {c_number} countries across {regions} geographical regions. It advertises {ipv4_number} IPv4
and {ipv6_number} IPv6 prefixes. It is present in {ix_count} public IXes worldwide, with a total of {link_count} peering links and
aggregated throughput of {agg_speed}bps.\n\n\n'''

reg_header = '''================================
================================
Region name: {r_name}. 
Present in {c_num} countries within the region.
Present in {ix_num} IX(es) within the region.
Aggregate speed within the region: {speed}bps
\n
'''


country_header = '''

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Country: {c_name}.
Number of IXes with  AS{asn} present: {ix_number}.
Aggregate speed in the country: {speed}bps

'''

ix_header = '''-------------------------------
IX name: {name}
Number of links in IX: {link_num}
Links details:\n'''

link_details = '''..............................
Link IPv4 address: {ipv4}
Links IPv6 address: {ipv6}
Link speed: {speed}\n'''