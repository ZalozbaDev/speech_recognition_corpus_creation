#!/usr/bin/perl -w

# quit unless we have the correct number of command-line args
$num_args = $#ARGV + 1;
if ($num_args != 1) {
    print "\nUsage: read_lexicon.pl lexicon_sampa.lex\n";
    exit;
}

$lexicon = $ARGV[0];

printf "Lexicon = %s.\n", $lexicon;

open(INHANDLE, "$lexicon") or die "Cannot open $lexicon for reading!\n";

@textual = ();
@phonetical = ();

$totallines = 0;

while (<INHANDLE>)
{
	$line = $_;
	chomp($line);
	($text,$phones) = $line =~ m/(.+)\t(.+)/;
	
	printf "#%s#\t&%s&\n", $text, $phones;
	
	push @textual, $text;
	push @phonetical, $phones;
	
	$totallines++;
}

close INHANDLE;

printf "Read %d lines from lexicon.\n", $totallines;

while (1)
{
	$myline = int(rand($totallines));
	
	# printf "Processing word %s with phonemes %s.\n", $textual[$myline], $phonetical[$myline];
	
	printf "Processing word %s:\n", $textual[$myline];
	
	@phones = split(" ", $phonetical[$myline]);
	
	# print join (", ", @phones);
	
	system("rm -f mbrola_input.pho mbrola_output.wav");
	
	open(OUTHANDLE, "> mbrola_input.pho") or die ("Cannot open output file for writing!\n");
	
	for ($index = 0; $index < scalar(@phones); $index++)
	{
		# printf "Processing %s.\n", $phones[$index];
		$outputline = $phones[$index];
		
		# map to phonemes of MBROLA "cz2" voice
		$outputline =~ s/E/e/;
		$outputline =~ s/I/i/;
		$outputline =~ s/O/o/;
		$outputline =~ s/U/u/;
		$outputline =~ s/w/v/;
		$outputline =~ s/h/h\\/;
		# $outputline =~ s/C/x/;
		# $outputline =~ s/1/i/;
		
		# add length of phoneme
		# mark those which are not "properly" mapped, e.g. where an "unexpected" phoneme might occur
		if (($outputline =~ m/a/) || ($outputline =~ m/e/) || ($outputline =~ m/i/) ||
			($outputline =~ m/o/) || ($outputline =~ m/u/))
		{
			$outputline = $outputline . "\t200";	
		}
		else
		{
			if ($outputline =~ m/1/)
			{
				$outputline = "; !!!! improvised mapping of 'y'!!!!\ni\t200\n; !!!! improvised mapping of 'y'!!!!";
			}
			elsif ($outputline =~ m/C/)
			{
				$outputline = "; !!!!improvised mapping of 'ch'!!!!\nx\t100\n; !!!!improvised mapping of 'ch'!!!!";
			}
			else
			{
				$outputline = $outputline . "\t100";	
			}
		}
		
		printf "%s\n", $outputline;
		print OUTHANDLE $outputline . "\n";
	}
	
	close OUTHANDLE;
	
	system("mbrola /usr/share/mbrola/cz2/cz2 mbrola_input.pho mbrola_output.wav");
	system("aplay mbrola_output.wav");
	
	WaitForKey();
}






sub WaitForKey() {
    print "\nPress any key to continue...";
    chomp($key = <STDIN>);
}
