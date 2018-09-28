import os
for root,dirs,files in os.walk('.'):
    for filename in files:
        if filename != 'md.py':
            mdfile = open(filename, 'r+')
            content = mdfile.read()
            content.replace('/images/', '/cdn/images/aosabook')
            mdfile.seek(0,0)
            mdfile.write('---\ntitle: ' + filename[:-3] \
            + '\ndate: 2018-09-28\ntags: aosabook\n' + content)
            mdfile.close()
        
#        print(filename)
