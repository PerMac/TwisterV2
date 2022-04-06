import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--generate-hardware-map',
        dest='hardware_map_path',
        metavar='path',
        help='generate hardware map',
    )

    args = parser.parse_args()

    if args.hardware_map_path:
        print('Not implemented')
        raise SystemExit(0)

    parser.print_help()
