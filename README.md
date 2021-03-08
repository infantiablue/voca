# voca

Builder App for CS50x final project

## Set Up

Install required packages:

    sudo apt install python3-dev libpq-dev python3-venv git nodejs npm openssl build-essential direnv nginx postgresql

Run the `psql` command from the postgres user account:

    sudo -u postgres psql postgres

Then set password

    \password postgres

Create Postgres DB

    CREATE DATABASE dbname;
    CREATE USER user WITH ENCRYPTED PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE user TO dbname;

Add SSH keys from [Github tutorial](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

    ssh-keygen -t ed25519 -C "dangtruong@gmail.com"

Clone from source

    git clone git@github.com:infantiablue/voca.git

Then crete VENV environemnt:

    python3 -m venv .env

Hook `direnv` to bash shell, by adding the line below to `~/.bashrc`:

    eval "$(direnv hook bash)"

 Modify app root path & domain name then include the conf file `config/nginx.conf` into `/etc/nginx/nginx.conf`

    ...
    server_name  voca.techika.com;
    error_log    /home/truong/voca/logs/nginx_error.log;
    ...

    location /static/ {
        alias /home/truong/voca/app/static/;
    }

Configure SSL

    sudo apt install software-properties-common
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d voca.techika.com

Create nginx conf file