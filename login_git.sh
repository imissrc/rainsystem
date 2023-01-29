#!/usr/bin/expect

set USER "imissrc"
set PASSWORD "rc66167978"

spawn git fetch --all

expect {
  "Username*: " { send "$USER\r"; exp_continue }
  "Password*: " { send "$PASSWORD\r" }
}
expect eof
