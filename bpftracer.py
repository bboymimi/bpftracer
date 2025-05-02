#!/usr/bin/env python3
"""BPFTracer - A tool for kernel debugging using bpftrace scripts.

This module provides a simple interface to run bpftrace scripts for kernel debugging
and analysis. It handles script execution, error checking, and output formatting.
"""

import os
import sys
import subprocess
import argparse


class BPFTracer:
    """A class to manage and execute bpftrace scripts for kernel debugging."""

    def __init__(self):
        """Initialize BPFTracer with script directory and run prerequisites check."""
        self.scripts_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'scripts'
        )
        self.check_prerequisites()

    def check_prerequisites(self):
        """Check if the script has necessary permissions and requirements.

        Raises:
            SystemExit: If the script is not run as root or bpftrace is not available
        """
        if os.geteuid() != 0:
            sys.exit("Error: This script must be run as root (sudo)")

        try:
            subprocess.run(
                ['bpftrace', '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            sys.exit("Error: bpftrace is not installed or not accessible")

    def run_bpftrace_script(self, script_name):
        """Run a specific bpftrace script.

        Args:
            script_name: Name of the bpftrace script to execute

        Raises:
            SystemExit: If the script file is not found
            Exception: If there's an error running the script
        """
        script_path = os.path.join(self.scripts_dir, script_name)
        if not os.path.exists(script_path):
            sys.exit(f"Error: Script {script_name} not found")

        try:
            # Read the script content
            with open(script_path, 'r') as f:
                script_content = f.read()

            # Set up environment with BPFTRACE_MAX_STRLEN
            env = os.environ.copy()
            env['BPFTRACE_MAX_STRLEN'] = '200'

            # Run bpftrace with the script content
            process = subprocess.run(
                ['bpftrace', '-q', '-e', script_content],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                check=True
            )
            print(process.stdout.strip())
            if process.stderr:
                print(
                    "Warnings/Errors:",
                    process.stderr.strip(),
                    file=sys.stderr
                )
        except subprocess.CalledProcessError as e:
            print(f"Error running bpftrace script: {e}", file=sys.stderr)
            if e.output:
                print("Output:", e.output.strip(), file=sys.stderr)
            if e.stderr:
                print("Stderr:", e.stderr.strip(), file=sys.stderr)
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)


def main():
    """Main entry point for the BPFTracer tool."""
    parser = argparse.ArgumentParser(
        description='BPFTracer - Kernel debugging tool using bpftrace'
    )
    parser.add_argument(
        '--script',
        default='kernel_info.bt',
        help='Name of the bpftrace script to run (default: kernel_info.bt)'
    )
    args = parser.parse_args()

    tracer = BPFTracer()
    tracer.run_bpftrace_script(args.script)


if __name__ == '__main__':
    main() 