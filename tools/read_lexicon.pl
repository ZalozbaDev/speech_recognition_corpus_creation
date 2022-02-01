#!/usr/bin/perl -w

use Term::ReadKey;

# quit unless we have the correct number of command-line args
$num_args = $#ARGV + 1;
if ($num_args < 1) {
    print "\nUsage: read_lexicon.pl lexicon_sampa.lex [mbrola_voice]\n";
    print "Example: ./read_lexicon.pl ../examples/ex3/output/hsb_sampa.lex de6\n";
    exit;
}

$lexicon = $ARGV[0];
$voice = "cz2";
if ($num_args > 1) {
	$voice = $ARGV[1];	
}

printf "Lexicon = %s, voice = %s.\n", $lexicon, $voice;

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

if ($voice eq "cz2")
{
	while (1)
	{
		$myline = int(rand($totallines));
		
		# printf "Processing word %s with phonemes %s.\n", $textual[$myline], $phonetical[$myline];
		
		printf "Processing word %s:\n", $textual[$myline];
		
		findAlternatives($textual[$myline], $myline);
						
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
			$outputline =~ s/O/o/;
			$outputline =~ s/w/v/;
			$outputline =~ s/h/h\\/;
			# $outputline =~ s/U/u/;
			# $outputline =~ s/I/i/;
			# $outputline =~ s/C/x/;
			# $outputline =~ s/1/i/;
	
			# if O is last phoneme, make it longer
			if (($index == (scalar(@phones) - 1)) && ($outputline =~ m/o/))
			{
				$outputline = "o:\t400";
			}
			# add length of phoneme
			# mark those which are not "properly" mapped, e.g. where an "unexpected" phoneme might occur
			elsif (($outputline =~ m/a/) || ($outputline =~ m/e/) || ($outputline =~ m/i/) ||
				($outputline =~ m/o/) || ($outputline =~ m/u/))
			{
				$outputline = $outputline . "\t200";	
			}
			else
			{
				if ($outputline =~ m/1/)
				{
					$outputline = "; !!!! improvised mapping of 'y'!!!!\ni\t100\n; !!!! improvised mapping of 'y'!!!!";
				}
				elsif ($outputline =~ m/I/)
				{
					$outputline = "; !!!! improvised mapping of 'Ě'!!!!\ni\t50\ne\t50\n; !!!! improvised mapping of 'Ě'!!!!";
				}
				elsif ($outputline =~ m/U/)
				{
					$outputline = "; !!!! improvised mapping of 'Ó'!!!!\nu\t50\n; !!!! improvised mapping of 'Ó'!!!!";
				}
				elsif ($outputline =~ m/C/)
				{
					$outputline = "; !!!!improvised mapping of 'ch'!!!!\nx\t100\n; !!!!improvised mapping of 'ch'!!!!";
				}
				elsif ($outputline =~ m/jn/)
				{
					$outputline = "; !!!!improvised mapping of 'ń'!!!!\nj\t50\nn\t50\n; !!!!improvised mapping of 'ń'!!!!";
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
		
		$repeatme = 1;
		while ($repeatme == 1)
		{
			system("aplay -q mbrola_output.wav");
	
			print "Press 'Enter' for next, any other key for repeat.\n";
			ReadMode('cbreak');
			$key = ReadKey(0);
			while (defined($dummy=ReadKey(-1))) {};
			ReadMode('Normal');
			
			if ($key =~ m/\n/) 
			{
				$repeatme = 0;	
			}
		}
		
		print "\n\n";
	}
}
elsif ($voice =~ m/de/)
{
	# de6 is best
	while (1)
	{
		$myline = int(rand($totallines));
		
		# printf "Processing word %s with phonemes %s.\n", $textual[$myline], $phonetical[$myline];
		
		($minentry, $maxentry) = findAlternatives($textual[$myline], $myline);
	
		$myline = $minentry;
		
		$alternatives = $maxentry - $minentry;
		
		$newword = 0;
		while ($newword == 0)
		{
			printf "Processing word %s:\n", $textual[$myline];
		
			if ($alternatives > 0) {
				printf "Phonemes(%d/%d): %s\n", $myline - $minentry + 1, $maxentry - $minentry + 1, $phonetical[$myline];
			} else {
				printf "Phonemes: %s\n", $phonetical[$myline];
			}
			
			@phones = split(" ", $phonetical[$myline]);
			
			# print join (", ", @phones);
			
			system("rm -f mbrola_input.pho mbrola_output.wav");
			
			open(OUTHANDLE, "> mbrola_input.pho") or die ("Cannot open output file for writing!\n");
			
			for ($index = 0; $index < scalar(@phones); $index++)
			{
				# printf "Processing %s.\n", $phones[$index];
				$outputline = $phones[$index];
				
				# map to phonemes of MBROLA "deX" voice
		
				# extra length for vowels
				if (($outputline =~ m/a/) || ($outputline =~ m/E/) || ($outputline =~ m/e/) || ($outputline =~ m/i/) ||
					($outputline =~ m/O/) || ($outputline =~ m/o/) || ($outputline =~ m/u/) || ($outputline =~ m/1/))
				{
					# remapping
					$outputline =~ s/o/o:/;
					$outputline =~ s/i/I/;
					$outputline =~ s/e/e:/;
					$outputline =~ s/u/U/;
					$outputline =~ s/1/Y/;
					
					$outputline = $outputline . "\t200";	
				}
				else
				{
					$outputline =~ s/w/v/;
					
					
					if ($outputline =~ m/I/)
					{
						$outputline = "; !!!! improvised mapping of 'Ě'!!!!\nI\t50\nE\t50\n; !!!! improvised mapping of 'Ě'!!!!";
					}
					elsif ($outputline =~ m/U/)
					{
						$outputline = "U\t50";
					}
					#elsif ($outputline =~ m/r/)
					#{
					#	$outputline = "6\t100";
					#}
					elsif ($outputline =~ m/jn/)
					{
						$outputline = "; !!!!improvised mapping of 'ń'!!!!\nj\t50\nn\t50\n; !!!!improvised mapping of 'ń'!!!!";
					}
					elsif ($outputline =~ m/dZ/)
					{
						# $outputline = "; !!!!improvised mapping of 'dź'!!!!\nd\t50\nZ\t50\n; !!!!improvised mapping of 'dź'!!!!";
						$outputline = "d\t50\nZ\t50";
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
		
			system("mbrola /usr/share/mbrola/$voice/$voice mbrola_input.pho mbrola_output.wav");
		
			system("aplay -q mbrola_output.wav");
	
			print "Press 'Enter' for new word, any other key for repeat/alternative.\n";
			ReadMode('cbreak');
			$key = ReadKey(0);
			while (defined($dummy=ReadKey(-1))) {};
			ReadMode('Normal');
			
			if ($key =~ m/\n/) 
			{
				$newword = 1;	
			}
			else
			{
				$myline++;	
				if ($myline > $maxentry)
				{
					$myline = $minentry;	
				}
			}
			
			print "\n";
		}
		
		print "-----------------------------------------------------\n\n";
	}
}
else
{
	die("Invalid voice $voice selected!\n");
}


sub WaitForKey() {
    print "\nPress any key to continue...";
    chomp($key = <STDIN>);
}

sub findAlternatives() {
	$word     = $_[0];
	$position = $_[1];
	
	$minimum = $position;
	$maximum = $position;
	
	# printf "Search for alternatives of %s at %d.\n", $word, $position; 
	
	# printf ("Lexicon entries:\n");
	
	while ($textual[$position] eq $word) {
		# printf "ALT!\n";
		$position--;
	}
	$position++;
	$minimum = $position;
	
	while ($textual[$position] eq $word) {
		#if ($position == $selected) {
			# printf "--> %s\n", $phonetical[$position];
		#} else {
			# printf "    %s\n", $phonetical[$position];
		#}
		$position++;	
	}
	$position--;
	$maximum = $position;
	
	return ($minimum, $maximum);
}
