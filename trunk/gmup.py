#!/usr/bin/python
# vim: ts=2 sw=2 et
# Note: this is equivalent to:
# vim: tabstop=2 shiftwidth=2 expandtab
#
# Original:
# sendmsg.py -- Demo to send a message via Gmail using libgmail
# $Revision: 1.4 $ ($Date: 2005/09/18 18:41:48 $)
# Author: follower@myrealbox.com
# License: GPL 2.0
#
# Hack revision:
# gmail_uploader.py
# Author: Ralfoide
# License: GPL 2.0
#
import os
import sys
import sha
import logging
import getopt
from stat import *

DEBUG = False
NLIMIT = -1
VERBOSE = False
DRY_RUN = False

# Allow us to run using installed `libgmail` or the one in a "libgmail" subdir.
try:
  import libgmail
  import lgconstants
  ## Wouldn't this the preffered way?
  ## We shouldn't raise a warning about a normal import
  ##logging.warn("Note: Using currently installed `libgmail` version.")
except ImportError:
  # Urghhh...
  sys.path.insert(1,
                  os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                "libgmail")))
  import libgmail
  import lgconstants

def verbose(msg, *args):
  global VERBOSE
  if VERBOSE:
    print msg % args

def usage_and_exit():  
  print """
Usage: %s [-apvnh] <dir1> .. <dirN>
Options:
  -a, --account=name  Account name
  -p, --password=pwd  Account password
  -v, --verbose       Verbose mode
  -n, --dry-run       Dry-run
  -h, --help          This help
""" % sys.argv[0]
  sys.exit(1)

def get_params():
  pw = None
  account = None
  optlist, args = getopt.gnu_getopt(sys.argv[1:],
                                    shortopts="p:a:vnhdl:",
                                    longopts=["account=",
                                              "password=",
                                              "verbose",
                                              "dry-run",
                                              "help",
																							"debug",
																							"limit="])
  for o, a in optlist:
    global VERBOSE, DEBUG, DRY_RUN, NLIMIT
    if o in ["-v", "--verbose"]:
      VERBOSE = True
    elif o in ["-n", "--dry-run"]:
      DRY_RUN = True
    elif o in ["-p", "--password"]:
      pw = a
    elif o in ["-a", "--account"]:
      account = a
    elif o in ["-h", "--help"]:
      usage_and_exit()
    elif o in ["-d", "--debug"]:
      DEBUG = True
      VERBOSE = True
    elif o in ["-l", "--limit"]:
      global NLIMIT
      NLIMIT = int(a)
  
  if not account:
    usage_and_exit()

  try:
    root_dirs = args
  except IndexError:
    usage_and_exit()
  
  if not pw:
    from getpass import getpass
    pw = getpass("Password for %s: " % account)
  
  return account, pw, root_dirs

def connect(name, pw):
  ga = libgmail.GmailAccount(name, pw)
  verbose("Please wait, logging in...")

  try:
    ga.login()
    verbose("Log in successful.\n")
    return ga
  except libgmail.GmailLoginFailure:
    verbose("Login failed. (Wrong username/password?)")
  return None

def get_files(initial_dirs):
  result = []
  for initial_dir in initial_dirs:
    for root_dir, dirs, files in os.walk(initial_dir):
      for file in files:
        if file.endswith(".jpg"):
          full = os.path.join(root_dir, file)
          result.append(pretty_filename(full, initial_dir))
  verbose("Found %d files" % len(result))
  return result

def pretty_filename(full_path, root_dir):
  fname = full_path
  if fname.startswith(root_dir):
    fname = fname[len(root_dir):]
  if fname.startswith("/"):
    fname = fname[1:]
  return (full_path, fname)

def process_files(ga, files, existing):
  n = len(files)
  for i in xrange(n):
    full, fname = files[i]

    if fname in existing:
      verbose("Skipping '%s' (%d of %d, %.2f%%)", fname, i + 1, n, 100.0 * i / n)
      continue

    subject = fname
    to = "%s@gmail.com" % ga.name
    size = os.stat(full)[ST_SIZE]
    f = file(full, "r")
    s = sha.new(f.read())
    digest = s.hexdigest()
    f.close()
    msg = """
PATH: \"%s\"
SIZE: %s
SHA: %s
""" % (fname, size, digest)
    gmsg = libgmail.GmailComposedMessage(to, subject, msg,
                                         filenames=[full])

    verbose("Sending '%s' (%d of %d, %.2f%%)", subject, i + 1, n, 100.0 * i / n)
    global DEBUG
    if DEBUG:
      verbose("# Gmail Message: %s", repr(gmsg.__dict__))

    global DRY_RUN, NLIMIT
    if not DRY_RUN:
      if ga.sendMessage(gmsg):
        verbose("Message sent `%s` successfully." % subject)
        if NLIMIT > 0:
          NLIMIT -= 1
          if NLIMIT == 0:
            sys.exit(0)
      else:
        verbose("Could not send message.")

def get_existing_files(ga):
  verbose("Retrieving list of existing files...")
  threads = ga.getMessagesByLabel(lgconstants.U_INBOX_SEARCH)
  files = {}
  for thread in threads:
    for msg in thread:
      files[msg.subject] = msg
  verbose("Retrieved %d messages", len(files))
  return files

def main():
  account, password, root_dirs = get_params()
  files = get_files(root_dirs)
  if files:
    ga = connect(account, password)
    if ga:
      existing = get_existing_files(ga)
      process_files(ga, files, existing)
  verbose("Done.")
  
if __name__ == "__main__":
  main()


