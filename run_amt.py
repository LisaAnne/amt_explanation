import os
import sys
import boto.mturk.connection
import boto.mturk.question
from boto.mturk.qualification import LocaleRequirement, PercentAssignmentsApprovedRequirement, Qualifications
import pdb
import datetime
import json
from private import *#this should have acces key and secret key.  Never share this!!!

sandbox_host = 'mechanicalturk.sandbox.amazonaws.com'
real_host = 'mechanicalturk.amazonaws.com'

class AMT(object):

    def __init__(self, sandbox=False):
        if sandbox:
          self.host = sandbox_host
        else:
          self.host = real_host
        self.mturk = boto.mturk.connection.MTurkConnection(
          aws_access_key_id = AWSAccessKeyId,
          aws_secret_access_key = AWSSecretKey,
          host = self.host,
          debug = 1) 
        self.frame_height = 2000

    def submit_hit(self, urls, title, description, keywords=None,
                   duration=datetime.timedelta(seconds=300), amount=0.0,
                   response_groups = ('Minimal', 'HITDetail'), num_assignments=5):

        quals = Qualifications()
        #mturk workers with high apporval in the US.
        approve_requirement = 95
        quals.add(PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", approve_requirement))
        quals.add(LocaleRequirement("EqualTo", "US"))

        hit_type = self.mturk.register_hit_type(title, description, boto.mturk.price.Price(amount = amount), duration, keywords, qual_req=quals, approval_delay=datetime.timedelta(seconds=100000))

        for requirement in quals.requirements:
            requirement.required_to_preview = True


        for url in urls:
            try:
                questionform = boto.mturk.question.ExternalQuestion( url, self.frame_height )
                create_hit_result = self.mturk.create_hit(
                    hit_type = hit_type[0].HITTypeId,
                    question = questionform,
                    max_assignments = num_assignments,
                    response_groups = ( 'Minimal', 'HITDetail' ),
                    qualifications = quals,
                    lifetime = datetime.timedelta(days=90)
                ) 
                assert create_hit_result.status
            except:
                 print "Could not finish making hits.  Check that you have enough money in the account!"

    def accept_assignments(self, assignment_ids):
        for assignment_id in assignment_ids: 
            self.mturk.approve_assignment(assignment_id)

    def reject_assignments(self, assignment_ids):
        for assignment_id in assignment_ids: 
            self.mturk.reject_assignment(assignment_id)

