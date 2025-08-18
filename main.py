from argparse import ArgumentParser, Namespace

from Classes.engine import Engine


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description='E-Semantic Analysis Tool')
    parser.add_argument('files', nargs='+', help='C files to compare')

    return parser.parse_args()


def main():
    main_engine = Engine()

    args = parse_arguments()

    main_engine.upload_user_files(args.files)

if __name__ == '__main__':
    main()
