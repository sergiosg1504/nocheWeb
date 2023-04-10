#!/usr/bin/perl
use Email::Send::SMTP::Gmail;
use DBI;
use Excel::Writer::XLSX;

my $f2 = "commands.txt";

my $excel = Excel::Writer::XLSX->new( 'stats.xlsx' );

my $ws = $excel->add_worksheet();
open my $info, $f2 or die "Could not open $fichero1: $!";

my @veces;
my @comandos;

while( my $line = <$info>)  {
        chomp $line;
        my @data = split / /, $line;
        @data = grep($_, @data);
        $data[8] =~ s/\s+//g;
        push(@comandos, $data[8]);
        $data[0] =~ s/\s+//g;
        chop($data[0]);
        push(@veces, $data[0]);
}

close $info;

# Add the worksheet data the chart refers to.
my $datosFichero = [
    [ 'Comandos', @comandos ],
    [ 'Veces',  @veces ]
];

$ws->write( 'A1', $datosFichero );

$chart = $excel->add_chart( type => 'pie', embedded => 1 );

# Configure the chart.
$chart->add_series(
    categories => [ 'Sheet1', 1, 60, 0, 0 ],
    values     => [ 'Sheet1', 1, 60, 1, 1 ],
);

$chart->set_title( name => '10 comandos mas veces llamados' );
$chart->set_style( 10 );
$chart->set_size( width => 800, height => 600 );

$ws->insert_chart( 'C2', $chart, 20, 20 );

$excel->close();

my $db=DBI->connect('dbi:mysql:database=nocheweb;host=localhost','administrador','admin') or die print("<p>el error es".DBI->errstr."</p>");
my $sth=$db->prepare('SELECT email FROM users WHERE is_admin=1') or warn $db->errstr;
$sth->execute() or die $sth->errstr;

my @r = $sth->fetchrow_array;
$sth->finish();

my $email = @r[0];

my $body = "Daily report from the server nocheWeb";
my ($mail,$error)=Email::Send::SMTP::Gmail->new(-smtp=>'smtp.gmail.com',-login=>'nocheweb22@gmail.com',-pass=>'jupgrafkgmunnebs');
print "session error $error" unless ($mail!=-1);
$mail->send(-to=>$email,-subject=>'daily report', -body=>$body, -attachments=>'stats.xlsx');
$mail-bye;