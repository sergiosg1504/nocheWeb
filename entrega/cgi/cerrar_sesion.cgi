#!/usr/bin/perl

use CGI;
use CGI::Session;

my $cgi = new CGI;

my $session= new CGI::Session;

$session->load();

$session->delete();
$session->flush();

print $cgi->header("text/html");
print "<meta http-equiv='refresh' content='0; /index.html'>";