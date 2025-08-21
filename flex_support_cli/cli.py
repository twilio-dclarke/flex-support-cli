#!/usr/bin/env python3
import sys
import argparse
import getpass
from flex_support_cli.config import load_config, save_profile, list_profiles
from flex_support_cli.clients import get_twilio_client
from flex_support_cli.io import create_report
from flex_support_cli.reports.taskrouter import taskrouter_queues, taskrouter_workers
from flex_support_cli.reports.conversations import get_conv_default_service, fetch_conv_addresses


def conversations_command(args):
    """Handle Conversations report generation."""
    username = args.cfg.username or 'token'
    password = args.cfg.password or args.token
    
    # Create Twilio client based on provided credentials
    if username and password:
        client = get_twilio_client(username=username, password=password)
    else:
        print("Error: You must provide either a token or username/password.")
        sys.exit(1)
    
    if args.conv_addresses:
        addresses = fetch_conv_addresses(client)
        file = create_report("conversation_addresses", args.cfg.profile, addresses)
        print(f"Conversation addresses report saved to {file}")
    else:
        print("No valid Conversations command provided.")   
def taskrouter_command(args):
    """Handle TaskRouter report generation."""
    workspace_sid = args.workspace_sid or args.cfg.workspace_sid
    username = args.cfg.username or 'token'
    password = args.cfg.password or args.token

    if not workspace_sid:
        print("Error: Workspace SID is required for TaskRouter operations.")
        sys.exit(1)
    
    # Create Twilio client based on provided credentials
    if username and password:
        client = get_twilio_client(username=username, password=password)
    else:
        print("Error: You must provide either a token or username/password.")
        sys.exit(1)

    if args.tr_queues and username == 'token':
        print("Support token not permitted for this operation")
        sys.exit(1)
    elif args.tr_queues:
        queues = taskrouter_queues(client=client, workspace_sid=workspace_sid)
        file = create_report("queue", workspace_sid, queues)
        print(f"Queue report saved to {file}")
    elif args.tr_workers:
        workers = taskrouter_workers(client=client, workspace_sid=workspace_sid)
        file = create_report("worker", workspace_sid, workers)
        print(f"Worker report saved to {file}")
    else:
        print("No valid TaskRouter command provided.")

def profile_command(args):
    """Handle profile management commands."""
    if args.create_profile:
        create_profile()
    elif args.list_profiles:
        profiles = list_profiles()
        print("Available profiles:")
        for profile in profiles:
            print(f"- {profile}")
    else:
        print("No valid profile command provided.")

def build_global_parser() -> argparse.ArgumentParser:
    """
    Parses only global options. We’ll run this first with parse_known_args().
    """
    g = argparse.ArgumentParser(add_help=False)
    g.add_argument("--profile", default="default", help="Config profile")
    g.add_argument(
        "--token",
        help="Optional runtime token override (e.g., TWILIO_AUTH_TOKEN or API Secret).",
    )
    g.add_argument(
        "--version",
        action="version",
        version="flex-support-exporter 0.1.0"
    )
    return g

def build_parser(parent: argparse.ArgumentParser) -> argparse.ArgumentParser:

    """"""
    p = argparse.ArgumentParser(
        prog="flex-support-cli",
        description="Flex Support CLI"
    )
    
    sp = p.add_subparsers(dest="command", required=True)

    """Profile management commands"""
    profile_parser = sp.add_parser("profiles", parents=[parent], help="Manage profiles")
    profile_parser.add_argument(
        "--create-profile",
        action="store_true",
        help="Create a new profile interactively"
    )
    profile_parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="Lists all profiles"
    )

    """TaskRouter report generation commands"""
    tr_parser = sp.add_parser("taskrouter", parents=[parent], help="TaskRouter reports")
    tr_parser.add_argument(
        "-w", "--workspace-sid",
        help="TaskRouter Workspace SID (default: from config)"
    )

    tr_parser.add_argument(
        "--tr-queues", 
        help="Generate TaskRouter queues report", 
        action="store_true"
    )
    tr_parser.add_argument(
        "--tr-workers", 
        help="Generate TaskRouter worker report", 
        action="store_true"
    )

    """Conversations report generation commands"""
    conv_parser = sp.add_parser("conversations", parents=[parent], help="Conversations reports")
    conv_parser.add_argument(
        "--conv-addresses", 
        help="Fetch conversation addresses", 
        action="store_true"
    )

    conv_parser.set_defaults(func=conversations_command)

    profile_parser.set_defaults(func=profile_command)
    tr_parser.set_defaults(func=taskrouter_command)
    
    return p

def create_profile():
    """Create a new profile with user input."""
    print("Creating a new profile...")
    name = input("Enter profile name: ")
    username = input("Enter Twilio Account SID: ")
    password = getpass.getpass("Enter Twilio Auth Token: ")
    print(len(username))
    if not username or not password:
        print("Username and password are required.")
        sys.exit(1)
    
    client = get_twilio_client(username=username, password=password)
   
    try:
        conv_service_sid = get_conv_default_service(client)
    except Exception as e:
        print(f"Invalid username and password combination {e}")
        sys.exit(1)

    workspace_sid = input("Enter TaskRouter Workspace SID: ")
    save_profile(name, USERNAME=username, PASSWORD=password, WORKSPACE_SID=workspace_sid, CONV_SERVICE_SID=conv_service_sid)

def main():

    """Main entry point for the CLI."""
    gparser = build_global_parser()
    gargs, unknown = gparser.parse_known_args()
    parser = build_parser(gparser)
    args = parser.parse_args()

    """Set up the configuration based on the provided profile or token."""
    if gargs.profile and gargs.profile != "default" :
        cfg = load_config(profile=gargs.profile)
    elif gargs.profile == "default" and args.command == "profiles":
        cfg = load_config()
    elif gargs.profile == "default" and gargs.token == None:
        print("Using default profile requires a support token")
        sys.exit(1)
    else:    
        cfg = load_config()

    args.cfg = cfg

    return args.func(args)

if __name__ == "__main__":
    main()