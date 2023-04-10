#!/usr/bin/perl

use DBI;
use Email::Send::SMTP::Gmail;

my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
my $sth=$db->prepare('SELECT email FROM users WHERE is_admin=1') or warn $db->errstr;
$sth->execute() or die $sth->errstr;

my @r = $sth->fetchrow_array;
$sth->finish();

my $email = @r[0];

my $body = "A root session has been started";
my ($mail,$error)=Email::Send::SMTP::Gmail->new(-smtp=>'smtp.gmail.com',-login=>'nocheweb22@gmail.com',-pass=>'jupgrafkgmunnebs');
print "session error $error" unless ($mail!=-1);
$mail->send(-to=>$email,-subject=>'WARNING ROOT SESSION', -body=>$body);
$mail-bye;