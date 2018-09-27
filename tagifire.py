import re, os
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'trans tag wrapper. Input the module names you want to modify./ Modules template folder will be scanned and modified recursively'

    
    def add_arguments(self, parser):
        parser.add_argument('module', nargs='+', type=str)
    


    def exclude_this(self, text_obj):
        exclude_patterns = ['http:','https:','ftp:']
        for a in exclude_patterns:
            if re.match(a, text_obj) :
                # print('false', text_obj)
                return False

        return True

    def include_this(self, text_obj):
        include_patterns = ['.jpg','.png','.svg','gif','.css','.js']
        for a in include_patterns:
            if text_obj.endswith(a):
                return True

        return False      


    def trans_tag(self, matchobj):
        # print(matchobj.groups())
        if matchobj.group(2):
            textobj = matchobj.group(2)
            if self.exclude_this(textobj):
                replace_line = ">{{% trans '{}' %}}<".format(textobj)
            else : 
                replace_line = matchobj.group(0)
        elif matchobj.group(4) != None:
            textobj = matchobj.group(4)
            if self.exclude_this(textobj):
                replace_line = 'alt="{{% trans \'{}\' %}}"'.format(textobj) 
            else : 
                # print('group 4')
                replace_line = matchobj.group(0)
        else:
            # print('empty')
            replace_line = matchobj.group(0)
        self.stdout.write(replace_line )
        return replace_line
    
    def static_tag(self, matchobj):
        if matchobj.group(2):
            if self.exclude_this(matchobj.group(2)) and self.include_this(matchobj.group(2)):
                replace_line = '{}=\"{{% static \'{}\' %}}\"'.format(matchobj.group(1) ,matchobj.group(2))
            else : 
                replace_line = matchobj.group(0)
        self.stdout.write(replace_line)
        return replace_line



    def handle(self, *args, **options):
        for url in options['module']:
            self.stdout.write(url, )
            module_url = url+'/templates/'
            if os.path.exists(module_url):
                PATH = os.path.join(module_url)
                for root,d_names,f_names in os.walk(PATH):
                    print( root, d_names, f_names)
                    for file in f_names:
                        if file.endswith(".html"):
                            file_path = root+'/'+file
                            with open (file_path, 'r' ) as f:
                                content = f.read()
                            content_new = re.sub('(>([^{}<>()]+\S)<)|(alt="(\w*)")', self.trans_tag, content, flags = re.M)
                            content_new = re.sub('(href|src|img)=\"([^{%].*?)\"', self.static_tag, content_new, flags = re.M)
                            f.close()
                            with open (file_path, 'w' ) as g:
                                g.write(content_new)
                            g.close()
                            self.stdout.write(self.style.SUCCESS('Successfully wrapped "%s"' % file_path))
            else:
                er_message = "module {} doesn't exist".format(url)
                self.stdout.write(er_message, )