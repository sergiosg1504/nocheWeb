#!/usr/bin/perl

use CGI;
use DBI;
use Sys::Hostname;
use MIME::Base64;
use Email::Send::SMTP::Gmail;

my $cgi = new CGI();
print $cgi->header();


my $username = $cgi->param("id");
my $password = $cgi->param("password");
my $Rpassword = $cgi->param("Rpassword");
my $name = $cgi->param("name");
my $surname = $cgi->param("surname");
my $address = $cgi->param("address");
my $phone = $cgi->param("phone");
my $email = $cgi->param("email");
my $role = $cgi->param("role");

my $local_email = $username."@".hostname;

#Checking if passwords are the same

if($password ne $Rpassword){
        print "<h1>Las contraseñas no coinciden, vuelve a introducir los datos</h1>";
        print "<meta http-equiv='Refresh' content='4; /registro.html' />"
}
else{
        if($username =~ m[^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$])
        {
                # Connection to the database
                my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
                my $sth=$db->prepare('SELECT id FROM users WHERE id=? or email=?') or warn $db->errstr;
                $sth->execute($username, $email) or die $sth->errstr;

                my $chk_id = $sth->fetchrow_array;
                $sth->finish();

                if(!$chk_id){
                        if ($address eq ''){
                                $address = undef;
                        }
                        if ($phone eq ''){
                                $phone = undef;
                        }
                        my $encode = encode_base64($password);
                        my $q = $db->prepare("insert into nocheweb.users(id,password,name,surname,address,phone,email,local_email,role) values (?,?,?,?,?,?,?,?,?)");
                        $q->execute($username,$encode,$name,$surname,$address,$phone,$email,$local_email,$role);
                        $q->finish();

                        my $body = ("<p>Hola, solo queda un paso para disfrutar de los servicios de nocheWeb</p> <a href='https://nocheweb/activacion.html?user=$username'> Pulsa aqui e introduzca sus credenciales</a>");
                        my ($mail,$error)=Email::Send::SMTP::Gmail->new(-smtp=>'smtp.gmail.com',-login=>'nocheweb22@gmail.com',-pass=>'jupgrafkgmunnebs');
                        print "session error $error" unless ($mail!=-1);
                        $mail->send(-to=>$email,-subject=>'Correo de confirmacion', -body=>$body, -contenttype=>'text/html');
                        $mail-bye;

                        print_true();
                        
                }else{
                        print_false();
                        print "<meta http-equiv='Refresh' content='4; /index.html' />"
                }
        }
        else{
                print_false2();
                print "<meta http-equiv='Refresh' content='4; /index.html' />"
        }
}

sub print_true(){
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
                <div class="div-center4">
                    <p style="color:black; background-color:white;"> Se va a enviar un email al correo para continuar con el registro <br>Por favor revise su bandeja de entrada y siga los pasos que se le indican en el correo</p>
                </div>
        </body>

    </html>';
}

sub print_false(){
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
                <p style="color:black; background-color:white;">El usuario o el email ya estan en uso, por favor inicie sesion con esas credenciales</p>
            </div>
    </body>

    </html>';
}

sub print_false2(){
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
            <div class="div-center4">
                <p style="color:black; background-color:white;">El nombre de usuario no tiene el formato correcto</p>
            </div>
    </body>

    </html>';
}
