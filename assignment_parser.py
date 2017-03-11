import os

completed_assignments = os.listdir('/var/www/amtexplanation/site/results/')
write_txt_file = 'assignments/assignments_test.txt'
write_txt = open(write_txt_file, 'w')
for assignment in completed_assignments:
    if not 'ASSIGNMENT_ID_NOT_AVAILABLE' in assignment:
        hit_id = assignment.split('_')[0]
        assignment_id = assignment.split('_')[1].split('.json')[0]
        write_txt.writelines('%s\n' %assignment_id) 
write_txt.close()


