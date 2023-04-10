#!/usr/bin/perl
use DBI;
use Email::Send::SMTP::Gmail;
use MIME::Base64;
use CGI;

my $cgi = new CGI;
print $cgi->header();

my $email = $cgi->param("email");

my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
my $sth=$db->prepare('SELECT id, password FROM users WHERE email=?') or warn $db->errstr;
$sth->execute($email) or die $sth->errstr;

my @r = $sth->fetchrow_array;
$sth->finish();

if (@r){
        my $id = @r[0];
        my $pwd = @r[1];

        my $decode = decode_base64($pwd);

        my $body = "<h1>Buenas, $id </h1> <p> Ha solicitado el recuerdo de contraseña, para la próxima vez apuntesela en un papel</p> <p>Su contraseña es: $decode </p><small> Att: Los administradores de nocheWeb</small>";
        my ($mail,$error)=Email::Send::SMTP::Gmail->new(-smtp=>'smtp.gmail.com',-login=>'nocheweb22@gmail.com',-pass=>'jupgrafkgmunnebs');
        print "session error $error" unless ($mail!=-1);
        $mail->send(-to=>$email,-subject=>'Recuerdo de credenciales', -body=>$body, -contenttype=>'text/html');
        $mail-bye;

        print_true();
        print "<meta http-equiv='refresh' content='3; /index.html'>";

}else{
        print_false();
        print "<meta http-equiv='refresh' content='3; /index.html'>";
}


sub print_true{
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
        <p><a href="javascript:history.back()"><strong> Volver</strong></a></p>
    </div>
    <img src="/images/espacio.png" />
    <div class="container2">
        <div class="div-center4">
            <p style="color:black; background-color:white;">Se ha enviado el correo al email indicado</p>
        </div>
</body>

</html>';
        
};

sub print_false{
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
        <p><a href="javascript:history.back()"><strong> Volver</strong></a></p>
    </div>
    <img src="/images/espacio.png" />
    <div class="container2">
        <div class="div-center4">
            <p style="color:black; background-color:white;">El correo no tiene ningún usuario asociado</p>
        </div>
</body>

</html>';
}