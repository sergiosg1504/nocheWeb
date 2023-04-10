#!/usr/bin/perl

use CGI;
use CGI::Session;
use Socket;
use DBI;
my $cgi = new CGI;
my $session= new CGI::Session;

$session->load();
my @args = $session->param;

if ($session->is_expired or @args eq 0){
        $session->delete();
        $session->flush();

        print $cgi->redirect("https://nocheweb");
}else{

        my $username = $session->param("username");

        my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
        my $sth=$db->prepare('SELECT is_admin FROM users WHERE id=?') or warn $db->errstr;
        $sth->execute($username) or die $sth->errstr;

        my $chk_id = $sth->fetchrow_array;
        $sth->finish();

        if ($chk_id){
                print $cgi->header();
                print_promt();


        }else{
                print $cgi->redirect("https://nocheweb");
        }
}

sub print_promt{
        my $https =check_status(443) ;
        my $sftp = check_status(1024);
        my $db= check_status(3306) ;
        my $smtp = check_status(25);
        my $ssh= check_status(1024);
        my $proxy = check_status(3128);
        print '<!DOCTYPE html>
             <html>
                        <head>
                                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                                <title>NocheWeb</title>
                                <link rel="stylesheet" href="styles.css">
                                <link rel="icon" href="/images/icon.png">
                        </head>
                        <body>
                        <div class="back-div">
                                <p><a href="javascript:history.back()"><strong>Volver</strong></a></p>
                        </div>
                        <img src="/images/espacio.png" />
                        <div class="container2">
                                <div class="div-center">
                                        <div class="title2">
                                                <h1>ESTADO DE LOS SERVICIOS</h1>
                                        </div>
                                        <div class="button2">';
                                                print $https;
                                                        print '<a class="btn-half">
                                                                        <p><strong>HTTPS</strong></p>
                                                                </a>
                                                        </div>';
                                                print $sftp;
                                                        print '<a class="btn-half">
                                                                        <p><strong>SFTP</strong></p>
                                                                </a>
                                                        </div>
                                        </div>
                                        <div class="button2">';
                                                print $db;
                                                        print '<a class="btn-half">
                                                                        <p><strong>MARIADB</strong></p>
                                                                </a>
                                                        </div>';
                                                print $smtp;
                                                        print '<a class="btn-half">
                                                                        <p><strong>SMTP</strong></p>
                                                                </a>
                                                        </div>
                                        </div>
                                        <div class="button2">';
                                                print $ssh;
                                                        print '<a class="btn-half">
                                                                        <p><strong>SSH</strong></p>
                                                                </a>
                                                        </div>';
                                                print $proxy;
                                                        print '<a class="btn-half">
                                                                        <p><strong>PROXY</strong></p>
                                                                </a>
                                                        </div>
                                        </div>
                                </div>
                        </div>
                    </body>
            </html>';
}

sub check_status{
        my ($port) = @_;
        ($name, $aliases, $protocol_number) = getprotobyname("tcp");
        socket(SOCKET, PF_INET, SOCK_STREAM, $protocol_number);

        if(connect( SOCKET, pack_sockaddr_in($port, inet_aton("localhost"))))
        {
                return ("<div class='btn3 green'>");
        }else{
                return ("<div class='btn3 red'>")
        }

}