#!/bin/bash

# Variables
TARGET_SERVER=$1
TICKET_ID=$2
REASON=$3
PSMP_USER="your_psmp_user"
PSMP_HOST="your_psmp_host"
ENCRYPTED_PASSWORD_FILE="password.enc"
PASSPHRASE="your_passphrase"  # Optionally prompt for the passphrase

# Check if required arguments are provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <target_server> <ticket_id> <reason>"
  exit 1
fi

# Decrypt the password using openssl
PASSWORD=$(openssl enc -aes-256-cbc -pbkdf2 -d -salt -in $ENCRYPTED_PASSWORD_FILE -pass pass:$PASSPHRASE)

if [ -z "$PASSWORD" ]; then
  echo "Failed to decrypt the password"
  exit 1
fi

# Expect script to automate the SSH process
expect <<EOF
  # Start the SSH connection to the PSMP host
  spawn ssh -l $PSMP_USER -oKexAlgorithms=+diffie-hellman-group14-sha1 $PSMP_HOST

  # Look for password prompt and provide it
  expect "password:"
  send "$PASSWORD\r"

  # Look for the prompt to enter the ticket ID
  expect "Ticket ID:"
  send "$TICKET_ID\r"

  # Look for the prompt to enter the reason
  expect "Reason:"
  send "$REASON\r"

  # Interact with the target server
  interact
EOF
