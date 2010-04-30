from skeleton import Skeleton, Var


class SimpleModule(Skeleton):
    src = 'basic-module'
    vars = [
        Var('ModuleName'),
        Var('Author'),
        Var('AuthorEmail'),
        ]


def main():
    SimpleModule().run()
    
if __name__ == '__main__':
    main()