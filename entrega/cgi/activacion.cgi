#!/usr/bin/perl
use CGI;
use CGI::Session;
use DBI;
use MIME::Base64;
use Linux::usermod;
use File::Copy::Recursive qw(dircopy);
use File::Path qw(make_path);
use Sudo;
use Email::Send::SMTP::Gmail;

my $cgi = new CGI();

print $cgi->header();

my $username = $cgi->param("id");
my $password = $cgi->param("password");
my $H_user = $cgi->param("hidden");

my $home_path = "/home/" . $username . "/";
my $skel = "/etc/skel";
# Check if the id and the hidden are the same

if( $username ne $H_user){
        print_false();
        print "<meta http-equiv='Refresh' content='4; /activacion.html?user=$H_user' />";
}
else{
        # Check if the user is in the database

        my $encode = encode_base64($password);
        my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
        my $sth=$db->prepare('SELECT id, role, email FROM users WHERE id=? and password=?') or warn $db->errstr;
        $sth->execute($username, $encode) or die $sth->errstr;

        my @chk_id = $sth->fetchrow_array;
        $sth->finish();

        if(@chk_id){
                # Create the user in the server
                        # Change state to 2
                my $q = $db->prepare("update nocheweb.users set state='2' where id=?");
                $q->execute($username);
                $q->finish();

                # Add the user to the passwd and shadow files
                        # Create the user in the files
                Linux::usermod->add($username, $password, '', '' ,'', $home_path, "/bin/bash");
                 my $user=Linux::usermod->new($username);
                        # Create the user group with the same gid that has added by default
                Linux::usermod->grpadd($username, $user->get('gid'));
                        # Get the created group
                my $gr = Linux::usermod->new($username, 1);
                        # Add the user to the group
                $gr->set(users,$username);
                # Create the Home Directory for the new user
                make_path($home_path, { owner => "gyermo", group => "gyermo" });
                # Copy the Skel Directory to the new Directory
                dircopy($skel, $home_path);

                # Add the new user to his group

                if (@chk_id[1] == 1){
                        my $grp_T = Linux::usermod->new("profesores", 230);

                        $usr_T = $grp_T->get(users);
                        my @usr_T_split = split(',', $usr_T);
                        push(@usr_T_split, $username);

                        $grp_T->set(users,"@usr_T_split");

                        my $file = "/empty/principal_profesor.html";
                        my $file_2 = "/empty/style.css";
                        my $dst = "/home/$username/pagina_personal/";

                        fcopy($file,$dst) or die $!;
                        fcopy($file_2,$dst) or die $!;

                        my $args_3 = "/home/$username/pagina_personal/principal_profesor.html /home/$username/pagina_personal/index.html";
                        my $su_mv = Sudo->new({
                                sudo            => '/usr/bin/sudo',
                                username        => 'root',
                                password        => 'compu',
                                program         => '/bin/mv',
                                program_args    => $args_3

                        });

                        $su_mv->sudo_run();
                }else{
                        my $grp_E = Linux::usermod->new("estudiantes", 231);
                                 $usr_E = $grp_E->get(users);
                        my @usr_E_split = split(',', $usr_E);
                        push(@usr_E_split, $username);

                        $grp_E->set(users,"@usr_E_split");
                        
                        my $file = "/empty/principal_estudiante.html";
                        my $file_2 = "/empty/style.css";
                        my $dst = "/home/$username/pagina_personal/";

                        fcopy($file,$dst) or die $!;
                        fcopy($file_2,$dst) or die $!;

                        my $args_3 = "/home/$username/pagina_personal/principal_estudiante.html /home/$username/pagina_personal/index.html";
                        my $su_mv = Sudo->new({
                                sudo            => '/usr/bin/sudo',
                                username        => 'root',
                                password        => 'compu',
                                program         => '/bin/mv',
                                program_args    => $args_3

                        });

                        $su_mv->sudo_run();
                }
                my $args_1 = "-R $username:$username /home/$username";
                my $su_1 = Sudo->new({
                        sudo            => '/usr/bin/sudo',
                        username        => 'root',
                        password        => 'compu',
                        program         => '/bin/chown',
                        program_args    => $args_1

                });

                my $result_1 = $su_1->sudo_run();


                my $args_2 = "-u $username 70M 80M 0 0 /home";
                my $su_2 = Sudo->new({
                        sudo            => '/usr/bin/sudo',
                        username        => 'root',
                        password        => 'compu',
                         program         => '/sbin/setquota',
                        program_args    => $args_2

                });

                my $result_2 = $su_2->sudo_run();

                print_propmt();
                my $email = @chk_id[2];


                my $body = ("<h1> El registro en nocheweb ha acabado correctamente</h1><p>Ya puede disfrutar de todos los servicios que le ofrecemos en <a href='https://nocheweb'> nocheWeb</a>");
                my ($mail,$error)=Email::Send::SMTP::Gmail->new(-smtp=>'smtp.gmail.com',-login=>'nocheweb22@gmail.com',-pass=>'jupgrafkgmunnebs');

                print "session error $error" unless ($mail!=-1);
                $mail->send(-to=>$email,-subject=>'Registro finalizado!!', -body=>$body, -contenttype=>'text/html');
                $mail-bye;

                my $session = new CGI::Session;
                $session->save_param($cgi);
                $session->expire("+1h");
                $session->flush();

                print "<meta http-equiv='refresh' content='1; redirect.cgi'>";
        }
        else{
                print "El usuario no esta en la base de datos, vuelve a intentarlo";
                print "<meta http-equiv='Refresh' content='4; /activacion.html?user=$H_user' />";
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
                                <p><a href="javascript:history.back()"><strong> Volver</strong></a></p>
                        </div>
                        <img src="/images/espacio.png" />
                        <div class="container2">
                                <div class="div-center4">
                                <p style="color:black; background-color:white;">El registro ha sido satisfactorio, se le va a redirigir a la aplicación</p>
                                </div>
                        </body>

                </html>';
}

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
            <p style="color:black; background-color:white;"><strong>El nombre de usuario no coincide con el token de registro, vuelva a intentarlo</strong></p>
        </div>
</body>

</html>';

}