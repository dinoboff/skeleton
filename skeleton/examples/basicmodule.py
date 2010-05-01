from skeleton import Skeleton, Var


class BasicModule(Skeleton):
    src = 'basic-module'
    vars = [
        Var('ModuleName'),
        Var('Author'),
        Var('AuthorEmail'),
        ]


def main():
    BasicModule().run()
    
if __name__ == '__main__':
    main()