#!/usr/bin/python

from app import app
from flask import request, jsonify, url_for, session
import os, requests
from app import mongo
from bson.objectid import ObjectId


def add_to_db(data_dict):
	#save data in mongo
	m_obj = mongo.db.annotation.insert(data_dict)
	
	#now compile author info
	author_db_build(data_dict)
	
	return m_obj


def author_db_build(data_dict):	
	target = data_dict['commentary'][0]['hasTarget']
	cite_urn = data_dict['commentary'][0]['hasBody']['@id']
	millnum = cite_urn.split('.')[2]
	t_parts = target.split(':')
	urn_parts = t_parts[3].split('.')
	pasg = t_parts[4]
	auth_id = urn_parts[0]
	work_id = ':'.join(t_parts[0:3]) + ':' + '.'.join(urn_parts[0:2])


	author = mongo.db.annotation.find_one({"cts_id" : auth_id})
	if author is None:
		url = "http://catalog.perseus.org/cite-collections/api/authors/search?canonical_id="+auth_id+'&format=json'
		response_dict = requests.get(url).json()
		for resp in response_dict:
			if resp['urn_status'] is not 'invalid':
				author = make_author(resp)

	works = author['works']
	if not works:		
		works.append(make_work(work_id, millnum, pasg))
	else:
		work = next((ent for ent in works if ent['cts_id'] == work_id), None)
		if work is None:
			works.append(make_work(work_id, millnum, pasg))
		else:
			if millnum not in work['millnums']:
				l = [millnum, pasg]
				work['millnums'].append(l)
	
	mongo.db.annotation.update({'_id' : author['_id']}, author)


def make_author(resp):
	author = {}
	author['name'] = resp['authority_name']
	author['cts_id'] = resp['canonical_id']
	author['works'] = []
	a_id = mongo.db.annotation.insert(author)
	new_auth = mongo.db.annotation.find_one({'_id' : a_id})
	return new_auth

def make_work(work_id, millnum, pasg):
	w_url = "http://catalog.perseus.org/cite-collections/api/works/search?work=" + work_id + "&format=json"
	w_resp = requests.get(w_url).json()
	for w in w_resp:
		if w['urn_status'] is not 'invalid':
			work = {}
			work['title']	= w['title_eng']
			work['cts_id'] = w['work']
			l = [[millnum, pasg]]
			work['millnums'] = l
			return work


						


