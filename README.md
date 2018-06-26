# NexusPHP-check-in
Scripts for check in websites powered by NexusPHP

## Install Dependencies
```bash
pip3 install -r requirements.txt
```

## Create your logins.conf
```bash
echo "website,login,password" >> logins.conf
```

**Caveat**: Do not include any resource identifier

eg. If the login page of the website is https://abc.com/login.php, you only need to enter https://abc.com as website

## Run
```bash
python3 sign.py
```
