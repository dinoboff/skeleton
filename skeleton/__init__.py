import os
import sys
import shutil



class Skeleton(object):
    src = None
    
    @property
    def skel_dir(self):
        if self.src is None:
            raise AttributeError("The src attribute of the %s Skeleton is not set" %
                self.__class__.__name__
                )
        mod = sys.modules[self.__class__.__module__]
        mod_dir = os.path.dirname(mod.__file__)
        return os.path.join(mod_dir, self.src)
    
    def write(self, dst_dir):
        skel_dir = self.skel_dir
        skel_dir_len = len(skel_dir)
        
        for dir_path, dir_names, file_names in os.walk(skel_dir):
            rel_dir_path = dir_path[skel_dir_len:].lstrip(r'\/')
            
            #copy files
            for file_name in file_names:
                src = os.path.join(dir_path, file_name)
                dst = os.path.join(dst_dir, rel_dir_path, file_name)
                shutil.copyfile(src, dst)
                shutil.copymode(src, dst)
            
            #copy directories
            for dir_name in dir_names:
                src = os.path.join(dir_path, dir_name)
                dst = os.path.join(dst_dir, rel_dir_path, dir_name)
                os.mkdir(dst)
                shutil.copymode(src, dst)


class Var(object):

    def __init__(self, name, description=None, default=None):
        self.name = name
        self.description = description
        self.default = default

    def __repr__(self):
        return '<%s %s default=%r>' % (
            self.__class__.__name__, self.name, self.default,)

    def full_description(self):
        if self.description:
            return '%s (%s)' % (self.name, self.description,)
        else:
            return self.name
        
    def prompt(self):
        prompt = 'Enter %s' % self.full_description()
        if self.default is not None:
            prompt += ' [%r]' % self.default
        prompt += ': '
        
        while True:
            resp = raw_input(prompt).strip()
            if resp != '':
                return resp
            elif self.default is not None:
                return self.default
            else:
                continue # persist asking