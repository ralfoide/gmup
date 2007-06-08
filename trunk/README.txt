=================
GMUP, a simple GMail Uploader

Author: ralfoide@gmail.com
License: GPL v2.0

=================
Summary:
Based on libgmail (cf http://libgmail.sf.net/), this is a simple rsync-like
tool to mirror files into gmail. The idea is to have one mail per file with the
mail as a regular attachment. The relative path of the file is the email's
subject.


DISCLAIMER: This tool is experimental and may or may not comply with the
GMail's user license. No guarantee of any kind is provided. Data and account
information is not handled securely. Loss of data may occur. Use at your own
risk. The usual stuff: if it's broken or doesn't work, please don't complain
about it. It's __experimental__. Don't expect what I cannot promise.

The bottom-line is that this is mostly for the fun. It's a pointless exercise
of uber futility. Storing data as email in gmail is probably the dumbest idea
I've ever had, but hey I wanted to do it a while ago and I finally had some time
to do it, so here I go. And apparently I'm not the only one to have this idea.
It's been done and redone and will be so for a while.

=================
Notes:

The purpose is to mirror a full directory, recursively, eventually with
file filters (extensions, exclusions.) Partial updates should skip files
which have already been uploaded, replace existing files that have changed
and delete files that have been deleted on the client side.

The obvious drawback is the "limited" storage space, which is currently 2.8 GB
total with 20 MB per mail. Email attachements are base64-encoded, which is
not space efficient (+50% encoded size, that is 2 bytes become 3 bytes.) This
means the current limit is about 1.8 GB total with 13 MB per file.

The obvious "benefit" of using regular attachements is that it's easy to
browse existing files using gmail's internal search. Images will be displayed
right away and files can be extracted easily. Separated words in filenames will
implicitely work as search keywords. Obviously this prevents encryption from
being used (at least not at the "protocol" layer). Also gmail refuses to
handle executable binary attachements.

Some alternatives & extensions may/could include:
* Create simples "cp" and "ls" tools. I believe this has already been done,
  and doesn't provide for a rsync-like functionality.
* Split files too large into several emails.
* Span over multiple accounts to have more storage.
* Use email threads for directories, one file per message in the same thread.

Sane people will of course note that to store images a better choice would
be to use a PicassaWeb account with the GData API. Next time.


=================
TODO:

20070608 Do not upload already uploaded files that are identical
20070608 "Replace" already uploaded files that have changed (remove first)
20070608 Delete files that are no longer on the client side
20070608 Command-line flags for extension filter and/or glob filter

=================
Done:

20070608 Support multiple source dirs
20070608 Do not upload already uploaded files
20070608 In each email, write the file size and a checksum (to detect changes)
20070608 Fix the broken _get_libgmail.sh (the login line won't work like this)
20070607 Very simple prototype using libgmail.demos.sendmsg.
20070607 Look at existing gmail-python libs. Selected libgmail.sf.net.
