#!/usr/bin/perl

use strict;
use warnings;

use utf8;
use File::Basename;
use List::Util qw(min);
use HTML::Entities;
use open ":std", ":encoding(UTF-8)";

my $timer = time();
my $path = dirname(__FILE__) . "/";

my %CONV;
open FILE, "<:encoding(UTF-8)", $path . "char_table.tsv"  or die $!;
while(<FILE>) {
    chomp;
    my ($a, $b) = split "\t", $_;
    $CONV{$a} = $b;
}
my $CONV_MAXLEN = length((sort { length($b) <=> length($a) } keys %CONV)[0]);

open FILE, "<:encoding(UTF-8)", $ARGV[0] or die $!;
while(<FILE>) {
    my $line = $_;

    # full width characters
    for my $i (0 .. length($line) - 1) {
        my $c = ord substr $line, $i, 1;
        if ($c >= 0xFF01 and $c <= 0xFF5E) {
            substr($line, $i, 1) = chr $c - hex "0xFEE0";
        }
    }

    # mixed width CJK characters
    for (my $i = 0; $i < length($line); ) {
        my $k = 1;
        for (my $j = min($CONV_MAXLEN, length($line) - $i); $j > 0; $j--) {
            my $w = substr $line, $i, $j;
            if (exists($CONV{$w})) {
                substr($line, $i, $j) = $CONV{$w};
                $k = 0;
                last;
            }
        }
        $i++ if $k;
    }

    # HTML entities
    $line = decode_entities($line);

    # control characters
    $line =~ s/[\x{0000}-\x{001F}\x{007F}\x{0080}-\x{009F}]+/ /g;

    # whitespace characters
    $line =~ s/[\x{0020}\x{00A0}\x{2000}-\x{200B}\x{202F}\x{205F}\x{3000}]+/ /g;

    # private use area
    $line =~ s/[\x{E000}-\x{F8FF}]+/ /g;

    # byte order marks
    $line =~ s/[\x{FEFF}\x{FFFE}]+/ /g;

    # punctuation marks
    $line =~ s/(?<=\S)’(?=(d|ll|m|re|s|t|ve)\b)/'/gi;

    $line =~ s/ {2,}/ /g;
    $line =~ s/^ | $//g;

    print $line, "\n";
}

printf STDERR "%f seconds\n", time() - $timer;
