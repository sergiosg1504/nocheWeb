#!/usr/bin/perl

use CGI;
use CGI::Session;
use Authen::Simple::PAM;

my $cgi = new CGI;

my $username = $cgi->param("username");
my $password = $cgi->param("password");

my $pam = Authen::Simple::PAM->new(
    service => 'login'
);

if ( $pam->authenticate( $username, $password ) ) {
        my $session = new CGI::Session;
        $session->save_param($cgi);
        $session->expire("+1h");
        $session->flush();

        print $session->header(-location => "redirect.cgi");
        print "<meta http-equiv='refresh' content='0; redirect.cgi'>";

}
else{
        print $cgi->redirect("https://nocheweb/index.html");
}