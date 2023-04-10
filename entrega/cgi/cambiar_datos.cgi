#!/usr/bin/perl

use CGI;
use CGI::Session;
use DBI;

my $cgi = new CGI;

my $session= new CGI::Session;

$session->load();

my @autenticar = $session->param;


if($session->is_expired or @autenticar eq 0){
        $session->delete();
        $session->flush();
        print $cgi->header("text/html");
        print "<meta http-equiv='refresh' content='0; /index.html'>";
}else{

        my $email =  $cgi->param("email");
        my $name = $cgi->param("name");
        my $surname = $cgi->param("surname");
        my $phone = $cgi->param("phone");
        my $address = $cgi->param("address");

        my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
        my $q=$db->prepare('SELECT * FROM users WHERE id=?') or warn $db->errstr;
        $q->execute($session->param("username"));

        my @datos = $q->fetchrow_array();
        $q->finish();

        if ($email eq ""){$email = @datos[7];}
        if ($name eq ""){$name = @datos[2];}
        if ($surname eq ""){$surname = @datos[3];}
        if ($phone eq ""){$phone = @datos[5];}
        if ($address eq ""){$address = @datos[4];}

        $q = $db->prepare('update nocheweb.users set email=?, name=?, surname=?, address=?, phone=? where id=?');
        $q->execute($email,$name,$surname,$address,$phone, $session->param("username"));
        $q->finish();

        my $state = @datos[6];
        my $admin = @datos[9];
        my $role = @datos[10];
        
        print $cgi->header();
        print_propmt();
        if ($state eq 2 and $admin eq 1){
                print "<meta http-equiv='Refresh' content='4; /admin.html' />"
        }elsif($state eq 2){
                if ($role eq 1){
                        print "<meta http-equiv='Refresh' content='4; /profesor.html' />"
                }else{
                        print "<meta http-equiv='Refresh' content='4; /estudiante.html' />"
                }
        }else{
                print "<meta http-equiv='Refresh' content='4; /index.html' />"
        }
}

sub print_propmt{
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
        <p><a href="javascript:history.back()"><strong> ← Volver</strong></a></p>
    </div>
    <img src="/images/espacio.png" />
    <div class="container2">
        <div class="div-center4">
            <p style="color:black; background-color:white;">Actualización realizada correctamente</p>
        </div>
</body>

</html>';

}