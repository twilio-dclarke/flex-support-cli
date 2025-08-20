#!/usr/bin/env python3
import os
import sys
import time
import argparse
from flex_support_cli.clients import get_twilio_client
from flex_support_cli.reports.taskrouter import taskrouter_queues, taskrouter_workers
from datetime import datetime, timedelta, timezone

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="flex-support-cli",
        description="Flex Support CLI"
    )
    p.add_argument(
        "-o", "--output",
        default="task_queues.csv",
        help="Output CSV path (default: task_queues.csv)"
    )
    p.add_argument(
        "--username",
        help="Twilio Account SID (overrides TWILIO_ACCOUNT_SID)."
    )
    p.add_argument(
        "--password",
        help="Twilio Auth Token (overrides TWILIO_AUTH_TOKEN)."
    )
    p.add_argument(
        "--workspace-sid",
        help="TaskRouter Workspace SID (overrides WORKSPACE_SID)."
    )
    p.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-error output."
    )
    p.add_argument(
        "--version",
        action="version",
        version="taskrouter-exporter 0.1.0"
    )
    p.add_argument(
        "--token",
        help="Support Token"
    )
    p.add_argument(
        "--tr-queues", 
        help="Generate TaskRouter queues report", 
        action="store_true"
    )
    p.add_argument(
        "--tr-workers", 
        help="Generate TaskRouter worker report", 
        action="store_true"
    )
    p.add_argument(
        "--months", 
        type=int, 
        default=6, 
        help="Inactivity window in months (default: 6)"
    )
    p.add_argument(
        "--page-size", 
        type=int, 
        default=50,
          help="Page size for listing workers/events (default: 50)"
        )
    return p



def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.token:
        client = get_twilio_client('token', password=args.token)
    elif args.username and args.password:
        client = get_twilio_client(username=args.username, password=args.password)
    else:
        parser.error("Error: You must provide either a token or username/password.")
        sys.exit(1)  

    if args.quiet:
        sys.stdout = open(os.devnull, 'w')

    if args.tr_queues:
        taskrouter_queues(client=client, workspace_sid=args.workspace_sid)
    elif args.tr_workers:
        taskrouter_workers(client=client, workspace_sid=args.workspace_sid)



if __name__ == "__main__":
    main()