#!/usr/bin/perl
use DBI;

my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin');
my $q = $db->prepare("delete from nocheweb.users where state=1");
$q->execute();
$q->finish();