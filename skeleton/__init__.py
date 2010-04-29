import codecs
import os
import shutil
import string
import sys


class Skeleton(dict):
    src = None
    Template = string.Template
    template_suffix = '_tmpl'
    file_encoding = 'UTF-8'
    
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
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self.Template(file_name).substitute(self))
                self.copy_file(src, dst)
            
            #copy directories
            for dir_name in dir_names:
                src = os.path.join(dir_path, dir_name)
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self.Template(dir_name).substitute(self))
                os.mkdir(dst)
                shutil.copymode(src, dst)
    
    def copy_file(self, src, dst):
        if src.endswith(self.template_suffix):
            dst = dst[:-len(self.template_suffix)]
            
            fd_src = None
            fd_dst = None
            try:
                fd_src = codecs.open(src, encoding=self.file_encoding)
                fd_dst = codecs.open(dst, 'w', encoding=self.file_encoding)
                fd_dst.write(self.Template(fd_src.read()).substitute(self))
            finally:
                if fd_src is not None:
                    fd_src.close()
                if fd_dst is not None:
                    fd_dst.close()
        else:
            shutil.copyfile(src, dst)
        shutil.copymode(src, dst)


class Var(object):

    def __init__(self, name, description=None, default=None):
        self.name = name
        self.description = description
        self.default = default

    def __repr__(self):
        return u'<%s %s default=%r>' % (
            self.__class__.__name__, self.name, self.default,)

    def full_description(self):
        if self.description:
            return u'%s (%s)' % (self.name, self.description,)
        else:
            return self.name
        
    def prompt(self):
        prompt = u'Enter %s' % self.full_description()
        if self.default is not None:
            prompt += u' [%r]' % self.default
        prompt += u': '
        
        while True:
            encoding = sys.stdout.encoding
            resp = raw_input(prompt.encode(encoding)).decode(encoding).strip()
            if resp:
                return resp
            elif self.default is not None:
                return self.default
            else:
                continue # persist asking
