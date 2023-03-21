#!/usr/bin/env perl

##  DemoExptServer.pl

##  This code from Chapter 15 of the book "Scripting with Objects"
##  by Avinash Kak

use strict;
use warnings;
use IO::Socket;                                                      #(A)
use Net::hostent;                                                    #(B)

my $server_soc = IO::Socket::INET->new( LocalPort => 9000,           #(C)
                                        Listen    => SOMAXCONN,      #(D)
                                        Proto     => 'tcp',          #(E)
                                        Reuse     => 1);             #(F)
die "No Server Socket" unless $server_soc;                           #(G)

print "[Server $0 accepting clients]\n";                             #(H)
while (my $client_soc = $server_soc->accept()) {                     #(I)
    print $client_soc "Welcome to $0; type help for command list.\n";#(J)
    my $hostinfo = gethostbyaddr($client_soc->peeraddr);             #(K)
    my $clientport = gethostbyaddr($client_soc->peerport);
    printf "\n[Connect from %s]\n", 
             $hostinfo ? $hostinfo->name : $client_soc->peerhost;    #(L)
    printf "[Client used the port %s]\n\n",     
             $clientport ? $clientport : $client_soc->peerport;
    print $client_soc "Command? ";                                   #(M)
    while ( <$client_soc> ) {                                        #(N)
        next unless /\S/;                                            #(O)
        printf "    client entered command: %s\n", $_;
        if    (/quit|exit/i) { last; }                               #(P)
	elsif (/date|time/i) { printf $client_soc "%s\n", 
                                              scalar localtime;}     #(Q)
        elsif (/ls/i )       { print  $client_soc `ls -al 2>&1`; }   #(R)
        elsif (/pwd/i )      { print  $client_soc `pwd 2>&1`;}       #(S)
        elsif (/user/i)      { print  $client_soc `whoami 2>&1`; }   #(T)
        elsif (/rmtilde/i)   { system "rm *~"; }                     #(U)
        else {                                                       #(V)
          print $client_soc 
             "Commands: quit exit date ls pwd user rmtilde\n";       #(W)
        }
    } continue {                                                     #(X)
        print $client_soc "Command? ";                               #(Y)
    }                                                                #(Z)
    close $client_soc;                                               #(a)
}
