#!/usr/bin/perl

use strict;
use warnings;
use utf8;

binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';

my %vocab;

while (my $line = <STDIN>) {
    foreach my $word ($line =~ m/[ \x{30A0}-\x{30FF}]+/g) {
        $word =~ s/・+/・/g;
        $word =~ s/^・|・$//g;
        $word =~ s/ {2,}/ /g;
        $word =~ s/^ | $//g;
        $vocab{$word} += 1 if $word;
    }
}

foreach my $word (sort {$vocab{$b} <=> $vocab{$a}} keys %vocab) {
    print $vocab{$word} . "\t" . $word . "\n";
}
