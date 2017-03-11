from run_amt import * 
import urllib
import pdb
import argparse

base_url = 'https://amtexplanation.berkeleyvision.org/'

parser = argparse.ArgumentParser()
parser.add_argument('--submit', dest='submit', action='store_true')
parser.set_defaults(submit=False)
parser.add_argument('--accept', dest='accept', action='store_true')
parser.set_defaults(accept=False)
parser.add_argument('--reject', dest='accept', action='store_true')
parser.set_defaults(accept=False)
parser.add_argument('--sandbox', dest='sandbox', action='store_true')
parser.set_defaults(sandbox=False)
#Text files with lists of images, tasks, or hits
parser.add_argument('--images', type=str, default=None)
parser.add_argument('--tasks', type=str, default=None)
parser.add_argument('--assignment_ids', type=str, default=None)

args = parser.parse_args()

if args.submit:
  assert args.images
  assert args.tasks

if args.accept:
  assert args.assignment_ids

if args.reject:
  assert args.assignment_ids
 
amt = AMT(sandbox=args.sandbox)

if args.submit:

    images = open(args.images).readlines()
    images = [i.strip() for i in images]
    tasks = open(args.tasks).readlines()
    tasks = [t.strip() for t in tasks]
  
    url_dicts = []
    for image, task in zip(images, tasks):
      url_dicts.append({'url': image, 'task': task})
    
    urls = [base_url + '?' + urllib.urlencode(url_dict) for url_dict in url_dicts]
    pdb.set_trace()
    amt.submit_hit(urls, "my test 2", "it's a test", num_assignments=1)
    print "Successfully submitted hits corresponding to images: %s and tasks: %s" %(args.images, args.tasks)

if args.accept:
    assignment_ids = open(args.assignment_ids).readlines()
    assignment_ids = [a.strip() for a in assignment_ids]
    amt.accept_assignments(assignment_ids)

if args.accept:
    assignment_ids = open(args.assignment_ids).readlines()
    assignment_ids = [a.strip() for a in assignment_ids]
    amt.reject_assignments(assignment_ids)


