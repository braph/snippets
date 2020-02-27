class Target:
    def __init__(self, name, depends=None, flags=None):
        self.name  = name
        if depends:     self.depends = set(depends.split())
        else:           self.depends = set()
        if flags:       self.flags = set([flags])
        else:           self.flags = set()

    def expand_depends(self, other_target):
        modified = False

        self.flags.update(other_target.flags)

        for dep in other_target.depends:
            if dep not in self.depends:
                self.depends.add(dep)
                modified = True
        return modified

    def __str__(self):
        r  = "%s.o: %s\n" % (self.name, ' '.join(self.depends))
        r += "\t$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c %s.cpp -o %s.o\n" % (self.name, self.name)
        return r

class Makefile:
    def __init__(self):
        self.targets = []

    def add(self, *target_args):
        self.targets.append(Target(*target_args))

    def generate(self):
        modified = True 
        while modified:
            modified = False
            for target in self.targets:
                for other_target in self.targets:
                    if target is other_target: continue
                    if other_target.name in target.depends:
                        modified = target.expand_depends(other_target)


    def printout(self):
        for target in self.targets:
            print(target)
            

makefile.add('xml',     '', '-l $(XML)')
makefile.add('config',  'xml')
makefile.add('theme', 'colors')
makefile.add('database', 'stringpool packedvector')
makefile.add('application', 'config database theme')
makefile.generate()
makefile.printout()

