#!/usr/bin/env python
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
import logging
import getopt

VERBOSE = False
DRY_RUN = False

# Allow us to run using installed `libgmail` or the one in a "libgmail" subdir.
try:
  import libgmail
  ## Wouldn't this the preffered way?
  ## We shouldn't raise a warning about a normal import
  ##logging.warn("Note: Using currently installed `libgmail` version.")
except ImportError:
  # Urghhh...
  sys.path.insert(1,
                  os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                "libgmail")))
  import libgmail

def verbose(msg, *args):
  global VERBOSE
  if VERBOSE:
    print "\n", msg % args

def usage_and_exit():  
  print """
Usage: %s [-pvnh] <account> <base_dir>
Options:
  -p, --password=pwd  Account password
  -v, --verbose       Verbose mode
  -n, --dry-run       Dry-run
  -h, --help          This help
""" % sys.argv[0]
  sys.exit(1)

def get_params():
  pw = None
  optlist, args = getopt.gnu_getopt(sys.argv[1:],
                                    shortopts="p:vnh",
                                    longopts=["password=",
                                              "verbose",
                                              "dry-run",
                                              "help"])
  for o, a in optlist:
    if o in ["-v", "--verbose"]:
      global VERBOSE
      VERBOSE = True
    elif o in ["-n", "--dry-run"]:
      global DRY_RUN
      DRY_RUN = True
    elif o in ["-p", "--password"]:
      pw = a
    elif o in ["-h", "--help"]:
      usage_and_exit()
  
  try:
    account = args[0]
    root_dir = args[1]
  except IndexError:
    usage_and_exit()
  
  if not pw:
    from getpass import getpass
    pw = getpass("Password for %s: " % account)
  
  return account, pw, root_dir

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

def get_files(initial_dir):
  result = []
  for root_dir, dirs, files in os.walk(initial_dir):
    for file in files:
      if file.endswith(".jpg"):
        full = os.path.join(root_dir, file)
        result.append(full)
  verbose("Found %d files" % len(result))
  return result

def process_files(ga, files, root_dir):
  for file in files:
    if file.startswith(root_dir):
      file = file[len(root_dir):]
    subject = file
    to = "%s@gmail.com" % ga.name
    msg = "\"%s\"" % file
    gmsg = libgmail.GmailComposedMessage(to, subject, msg,
                                         filenames=[file])

    verbose("Sending '%s'", subject)
    # Debug
    verbose("# Gmail Message: %s", repr(gmsg.__dict__))

    global DRY_RUN
    if not DRY_RUN:
      if False: ##ga.sendMessage(gmsg):
        verbose("Message sent `%s` successfully." % subject)
      else:
        verbose("Could not send message.")

def main():
  account, password, root_dir = get_params()
  files = get_files(root_dir)
  if files:
    ga = connect(account, password)
    if ga:
      process_files(ga, files, root_dir)
  verbose("Done.")
  
if __name__ == "__main__":
  main()



