#!/usr/bin/env python2.7

import datetime as dt
from peeringdb import PeeringDB
pdb = PeeringDB()

class Peering_report:
	def __init__(self,asn):
		self.asn = asn
		self.time = dt.datetime.now().ctime() 
		self.org_by_asn = pdb.all('net', asn=self.asn)[0]
		self.org_id = self.org_by_asn['id']
		self.peerings_raw = pdb.get('net', self.org_id)[0]
		self.name = self.org_by_asn['name']
		self.aka = self.org_by_asn['aka']
		self.ipv4_count = self.org_by_asn['info_prefixes4']
		self.ipv6_count = self.org_by_asn['info_prefixes6']
		self.site = self.org_by_asn['website']
		self.ix_link_list = self.peerings_raw['netixlan_set']
		self.link_count = len(self.ix_link_list)
		print "{} peering links found. Clarifying some details. This may take a couple of minutes...".format(self.link_count)
		self.ix_dict = self.get_ix_data()
		self.country_list = self.get_country_list()
		self.region_list = self.get_region_list()	
		self.agg_speed = self.get_agg_speed()
		self.region_count = len(self.region_list)
		self.country_count = len(self.country_list)
		self.ix_count = self.get_ix_count()
	def ix_link_analyzer(self, ix_link):
		ix_raw = pdb.get('ix', ix_link['ix_id'])[0]
		return {'ix_id':ix_link['ix_id'], 'name':ix_link['name'], 'speed':ix_link['speed'], 'ipv4':ix_link['ipaddr4'], 'ipv6':ix_link['ipaddr6'], 'country':ix_raw['country'], 'region':ix_raw['region_continent']}
	def get_ix_data(self):
		ix_list = []
		ix_dict = {}
		for ix_link in self.ix_link_list:
			ix_data = self.ix_link_analyzer(ix_link)
			if ix_data['region'] not in ix_dict.keys():
				ix_dict.update({ix_data['region']:{}})
			if ix_data['country'] not in ix_dict[ix_data['region']].keys():
				ix_dict[ix_data['region']].update({ix_data['country']:{}})
			if ix_data['ix_id'] not in ix_dict[ix_data['region']][ix_data['country']].keys():
				ix_dict[ix_data['region']][ix_data['country']].update({ix_data['ix_id']:{'name':ix_data['name'], 'links':[{'ipv4':ix_data['ipv4'], 'ipv6':ix_data['ipv6'], 'speed': ix_data['speed']}]}})
			else:
				ix_dict[ix_data['region']][ix_data['country']][ix_data['ix_id']]['links'].append({'ipv4':ix_data['ipv4'], 'ipv6':ix_data['ipv6'], 'speed': ix_data['speed']})
		return ix_dict
	def get_agg_speed(self):
		agg_speed = 0
		for region, country in self.ix_dict.iteritems():
			for country, ix in country.iteritems():
				for ix, ix_details in ix.iteritems():
					for link in ix_details['links']:
						agg_speed += link['speed']
		return agg_speed
	def get_country_list(self):
		c_list = []
		for region, country in self.ix_dict.iteritems():
			for country, ix in country.iteritems():
				c_list.append(country)
		return c_list
	def get_region_list(self):
		return self.ix_dict.keys()
	def peerings_per_region(self, region):
		if region in self.region_list:
			return self.ix_dict[region]
		else:
			return None
	def peerings_per_country(self, country):
		if country in self.country_list:
			for region, c in self.ix_dict.iteritems():
				if country in c.keys():
					return self.ix_dict[region][country]
		else:
			return None
	def speed_per_region(self, region):
		agg_speed = 0
		if region in self.region_list:
			for country, ix in self.ix_dict[region].iteritems():
				for ix, ix_details in ix.iteritems():
					for link in ix_details['links']:
							agg_speed += link['speed']
		else:
			return None
		return agg_speed
	def speed_per_country(self, country):
		agg_speed = 0
		if country in self.country_list:
			for region, c in self.ix_dict.iteritems():
				if country in c.keys():
					for ix, ix_details in self.ix_dict[region][country].iteritems():
						for link in ix_details['links']:
							agg_speed += link['speed']
		else:
			return None
		return agg_speed
	def get_ix_count(self):
		ix_count = 0
		for region, country in self.ix_dict.iteritems():
			for country, ix in country.iteritems():
				ix_count += len(ix)
		return ix_count
	def ix_count_per_region(self, region):
		return len(self.peerings_per_region(region))
	def ix_count_per_country(self, country):
		return len(self.peerings_per_country(country))