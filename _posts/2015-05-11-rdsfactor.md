---
layout: post
title: "RDS Factor: Two-factor auth for Microsoft Remote Desktop Services"
---



One month ago, during the deployment of a Remote Desktop Services
(RDS) installation, a major suprise of RDS came to my attention: The
RD Gateway is always open for basic username / password login. I
falsely assumed that RDS, like Citrix, would bring state between the
gateway and the web component, ensuring that a user has logged into RD
Web before giving access through the gateway.

To satisfy the security policy of most organizations, today I'm
announcing [RDS Factor](https://github.com/jakobadam/RDSFactor): An
open source two-factor component for Windows 2012 RDS.

## Two-factor authentication

RDS Factor alters the authentication procedure of RD Web and adds in a
second step, after username / password login. This step sends out an
SMS to the user after they've authenticated. The SMS contains a key
which when entered, allow them entrance to RD Web.

Clicking on an application in RD Web opens a window in the gateway for
that user. In that way, users that are not authenticated via RD Web
cannot access the RD Gateway.

## Securing the gateway

RDS Factor uses the RADIUS protocol for maintaining state between RD
Gateway, RD Web and the RDP client. When RDS Factor is in place the
gateway is only open for new connections from the RDP client when a
user clicks on an application in RD Web. Immediately after the Windows
application is launced, or after a timeout, the RD Gateway is again
closed for new connections. The overall flow that RDSFactor adds is
depicted below:

![RDSFactor Flow](/assets/rdsfaktor.png)

## Using RDS Factor with arbitrary authenticators

From the depiction of the overall flow it should be clear that the
second authentication factor using SMS is optional. This is relevant
in cases where you need to add other mechanisms for authentication,
but don't want to leave the gateway open for basic username / password
login.

We have RDS deployments in place where a custom two-factor login
server is put in front of RD Web. That setup would be pointless
without RDS Factor guarding the gateway.

RDSfactor is also part of our one-click deployment solution for RDS
available at: [origo.io](https://origo.io)
