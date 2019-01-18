---
layout: post
---

*I'll show how to obtain a certificate with letsencrypt and how to add it Postfix and Dovecot. As a side effect it fixes mail-sending in Wordpress.*

Dammit. An `apt-get upgrade` broke mail sending from Wordpress. The setup is similar to the one covered in [Tutorial: Use personal gmail with @yourdomain.com](/tutorial-use-personal-gmail-with-yourdomain), but basically, it's like this: mails are sent using a local Postfix instance and Dovecot is used for SMTP authentication.

Investigating the mail log shed a little light on the cause:

<center><small>/var/log/mail.log</small></center>
```
Apr  4 14:51:32 garagehaven postfix/smtpd[6856]: SSL_accept error from localhost[127.0.0.1]: 0
Apr  4 14:51:32 garagehaven postfix/smtpd[6856]: warning: TLS library problem: error:14094418:SSL routines:SSL3_READ_BYTES:tlsv1 alert unknown ca:s3_pkt.c:1262:SSL alert number 48:
```

Clearly the problem was related to SSL. To dig further, I created the following Wordpress mail sending test.


<small><center>wordpress/mail-test.php</center></small>
```
<?php
  require( dirname( __FILE__ ) . '/wp-blog-header.php' );

  $message = 'test'; 
  wp_mail( 'jakob@example.com', 'subject', 'message');
?>
```

And ran it with hhvm.
```
$ hhvm mail-test.php
Warning: SSL operation failed with code 1. OpenSSL Error messages:
error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed in /srv/www/garagehaven/wp-includes/class-smtp.php on line 344
```

The certificate can't be verified, and some PHP code chokes. This is no surprise, because, shame on me, I used a self-signed certificate. Luckily, with [letsencrypt.org](http://letsencrypt.org) we can now obtain a certificate. This is how to install it.

## Obtaining a certificate with letsencrypt

Check out the letsencrypt tool from github
```
sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt
```

### Create certificate

```
/opt/letsencrypt/letsencrypt-auto certonly -a webroot --webroot-path=/srv/www/garagehaven -d garagehaven.dk
```

Wait. Was that it? How did letsencrypt know that we are indeed on that domain. Easy, it added a file to the webroot. Fetched it and voila – a once so painful process eliminated. 

## Add certificate to Postfix and Dovecot

Update Postfix
```
postconf 'smtpd_tls_key_file = /etc/letsencrypt/live/garagehaven.dk/privkey.pem'  
postconf 'smtpd_tls_cert_file = /etc/letsencrypt/live/garagehaven.dk/cert.pem'  
postconf 'smtpd_tls_CAfile = /etc/letsencrypt/live/garagehaven.dk/chain.pem'  
```

Update Dovecot 
<small><center>/etc/dovecot/conf.d/10-ssl.conf</center></small>
```
ssl_cert = </etc/letsencrypt/live/garagehaven.dk/cert.pem  
ssl_key = </etc/letsencrypt/live/garagehaven.dk/privkey.pem  
```
And reload the services
```
$ postfix reload
$ dovecot reload
```
And Wordpress can now send mails again.

### Update certificate automatically with CRON

The certificate times out after 90 days. Thus, it's essential to automate updates. But, that's easy with cron and letsencrypt.
```
$ crontab -e
1 3 * * 1 /opt/letsencrypt/letsencrypt-auto renew >> /var/log/le-renew.log  
5 3 * * 1 /etc/init.d/postfix reload  
10 3 * * 1 /usr/sbin/dovecot reload  
```
Every monday at 3am, certificates are checked and renewed if stale.

## Summary
No fiddling with openssl. No pasting signatures into a CA. No frustration. Just one simple command to rule them all. Letsencrypt people – you rock!

