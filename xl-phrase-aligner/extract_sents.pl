#!/usr/bin/perl

use strict;
use warnings;
use utf8;

binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';

my @block;
my %sents;

while (my $line = <STDIN>) {

    chomp($line);

    if ($line ne "") {
        push(@block, $line);
        next;
    }

    my $sent = $block[0];
    my $score = (split "\t", $block[3])[1];
    $sents{$sent} = $score;
    @block = ();
}

foreach my $sent (sort {$sents{$b} <=> $sents{$a}} keys %sents) {
    my $score = $sents{$sent};
    print "$score\t$sent\n";
}
