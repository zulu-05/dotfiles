# Cheatsheet: `pass` (The Standard Unix Password Manager)

`pass` is a simple, secure password manager that follows the Unix philosophy. It uses GPG for encryption and stores passwords in a `~/.password-store` directory, which is itself a Git repository. This makes it incredibly powerful and easy to sync across multiple machines.

## One-Time Initialisation

You only need to do this once per machine to set up your password store.

### 1. Find your GPG Key ID:

You need to tell `pass` which GPG key to use for encrypting your secrets.

```bash
# List your secret keys in a long format to see the full ID 
gpg --list-secret-keys --keyid-format=long 

# The output will look something like this. The ID is the long string after the slash. 
# sec rsa4096/A1B2C3D4E5F6G7H8 2025-07-25 [SC]
```
### 2. Initialise the Password Store:

Use the GPG Key ID you just found to initialize the store.

```bash
pass init "A1B2C3D4E5F6G7H8"
```
### 3. (Optional but Recommended) Initialise as a Git Repository:

This is the key to syncing your passwords.

```bash
# Navigate into the newly created password store 
cd ~/.password-store 

# Initialize it as a git repository 
git init 

# Add a remote (e.g., a private repository on GitHub) 
git remote add origin git@github.com:your-user/my-password-store.git
```

## Core Commands

|Command|Description|
|---|---|
|`pass` or `pass ls`|**Lists** all passwords in a tree-like structure.|
|`pass [name]`|**Shows** a password. By default, it copies the password to the clipboard for 45 seconds and prints it to the screen.|
|`pass insert [name]`|**Inserts** a new password. `pass` will prompt you to type the password twice.|
|`pass generate [name] [len]`|**Generates** a new, secure random password of `len` characters and saves it. This is the best way to create new passwords.|
|`pass edit [name]`|**Edits** an existing password entry. This opens the GPG-encrypted file in your default `$EDITOR`.|
|`pass rm [name]`|**Removes** a password entry.|
### Practical Examples

#### Adding and Generating Passwords

You can organize passwords into subdirectories, which is highly recommended.

```bash
# Insert a password for Google. This will create a file at: 
# ~/.password-store/Email/google.gpg 
pass insert Email/google.com 

# Generate a secure 24-character password for AWS 
pass generate Services/aws 24 

# Generate a password with no symbols (-n) 
pass generate -n Services/heroku 30
```

#### Multi-line Entries

When you use `insert` or `edit`, the first line is always treated as the password itself. Any subsequent lines are stored with it and can be used for notes, usernames, security questions, etc.

```bash
# Use the -m flag for a multi-line entry 
pass insert -m Services/database 

# Your editor will open. You can enter text like this: 
# 
# MyS3cur3P@ssw0rd! <-- This first line is the password 
# User: db_admin 
# Host: db.example.com:5432 
# Notes: Remember to rotate this key quarterly.
```

When you `pass show Services/database`, it will copy `MyS3cur3P@ssw0rd!` to the clipboard but print the entire contents of the file to the screen.

#### Retrieving Passwords

```bash
# Show and copy the password for google.com 
pass Email/google.com 

# Show a password but DO NOT copy it to the clipboard (-c) 
pass -c Email/google.com
```
#### Git Integration

`pass` has built-in wrappers for Git, making syncing seamless.

```bash
# See what has changed since your last sync 
pass git status 

# Add a new password and commit it with a default message 
pass insert Services/new-service 
# pass will automatically run 'git add' and 'git commit' 

# Push your changes to the remote repository 
pass git push 

# Pull changes from another machine 
pass git pull
```