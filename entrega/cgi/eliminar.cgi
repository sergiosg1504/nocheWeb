#!/usr/bin/perl


use Linux::usermod;
use DBI;
use CGI;
use CGI::Session;
use Sudo;

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
        my $username = $session->param("username");

        my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
        my $sth=$db->prepare('SELECT id, is_admin, role FROM users WHERE id=?') or warn $db->errstr;
        $sth->execute($username) or die $sth->errstr;

        my @chk_id = $sth->fetchrow_array;
        $sth->finish();

        if(@chk_id){

                my $role = @chk_id[2];
                my $admin = @chk_id[1];
                if($admin eq 1){

                        print $cgi->header("text/html");
                        print "<meta http-equiv='refresh' content='0; /admin.html'>";
                }
                else{

                        if ($role eq 1){
                                my $g = Linux::usermod->new("profesores",1);
                                my $users = $g->get(users);
                                my @split = split(",", $users);

                                my @matched = grep {/$username/} @split;
                                if (@matched ne 0){
                                        my $i = 0;

                                        foreach $a (@split){
                                               if ($a eq $username){
                                                        last;
                                                }
                                                $i++;
                                        }
                                        splice(@split, $i,1);
                                        $g->set(users,"@split");
                                }
                        }elsif($role eq 2){
                                my $g = Linux::usermod->new("estudiantes",1);
                                my $users = $g->get(users);
                                my @split = split(",", $users);

                                my @matched = grep {/$username/} @split;
                                if (@matched ne 0){
                                        my $i = 0;

                                        foreach $a (@split){
                                               if ($a eq $username){
                                                        last;
                                                }
                                                $i++;
                                        }
                                        splice(@split, $i,1);
                                        $g->set(users,"@split");
                                }
                        }

                        Linux::usermod->del($username);
                        Linux::usermod->grpdel($username);

                        my $args = "-r /home/$username";
                        my $sudo_rm = Sudo->new({
                                sudo         => '/usr/bin/sudo',
                                username     => 'root',
                                password     => 'compu',
                                program      => '/bin/rm',
                                program_args => $args,
                        });

                        $sudo_rm->sudo_run();

                        $q=$db->prepare("delete from nocheweb.users where id=?");
                        my $r = $q->execute($username);
                        $q->finish();

                        $session->delete();
                        $session->flush();
                        print $cgi->header("text/html");
                        print "<meta http-equiv='refresh' content='0; /index.html'>";
                }
        }
        else{
                print $cgi->header("text/html");
                print "<meta http-equiv='refresh' content='0; /index.html'>";
        }
}