#!/usr/bin/perl

use CGI;
use CGI::Session;
use Sudo;

my $cgi = new CGI;
my $session= new CGI::Session;

$session->load();
my @args = $session->param;

if ($session->is_expired or @args eq 0){
        $session->delete();
        $session->flush();

        print $cgi->redirect("https://nocheweb");
}else{
        my $flag = 0;

        my $username = $session->param("username");
        my $directory = "/home/$username";
        #print $cgi->header();
        #print $directory;

        opendir (DIR, $directory) or die $!;

        while (my $file = readdir(DIR)) {

                if ($file eq "public_html"){
                        $flag=1;
                        last;
                }

        }
        closedir(DIR);
        if ($flag){
                print $cgi->redirect("https://nocheweb/~$username");
        }
        else{
                print $cgi->redirect("https://nocheweb/profile.html");
        }
}