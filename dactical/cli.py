import argparse
from dactical.replay.splunk import SplunkReplay

def main():
    parser = argparse.ArgumentParser(description='Dactical')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    replay_parser = subparsers.add_parser('replay', help='Replay the test data associated with the detections into a given SIEM')
    replay_parser.add_argument('-d', '--directory', help='The directory containing the detections', required=True)
    replay_parser.add_argument('-b', '--backend', help='The SIEM to replay the detections into e.g. splunk, elastic, etc.', required=True)

    test_parser = subparsers.add_parser('test', help='Test a given detection with a given SIEM')
    test_parser.add_argument('-f', '--file', help='The path to the detection to test', required=True)
    test_parser.add_argument('-b', '--backend', help='The SIEM to use e.g. splunk, elastic, etc.', required=True)

    lint_parser = subparsers.add_parser('lint', help='Lint a given rule file or directory of rules')
    lint_parser.add_argument('-d', '--directory', help='The directory containing the detections', required=True)

    args = parser.parse_args()

    if args.command == 'replay':
        if args.backend == 'splunk':
            replay = SplunkReplay('localhost', 'admin', 'asdfASDF1234')
        
        if replay.load_test_files(args.directory):
            replay.run()

        pass
    elif args.command == 'lint':
        # Handle lint command
        pass
    else:
        parser.print_help()

if __name__ == '__main__':
    main()