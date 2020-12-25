# IACR-EPRINT-UPDATE ![](https://github.com/InfiniteSynthesis/iacr-eprint-push/workflows/SEND%20UPDATE/badge.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-pink.svg)

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)

## Features 🚀

Weekly pushes the updates on [IACR ePrint Archive](https://eprint.iacr.org/) to your email. You can specify the topics.

The receivers and their topics of interest are stored in `users.json`. E.g.:

```json
{
    "receiver": "shenyu.tcv@gmail.com",
    "keywords": [
        "blockchain",
        "bitcoin"
    ]
}
```

> Keywords should be in lowercase.

## How to Use 🍕

- Add your name and topics of interest in `users.json`, then send me a MR.

- (Or,) fork this repo, set the users list (remove me), add the account name and password of an email address to Github Secrets as `SENDER_USERNAME` and `SENDER_PASSWORD`.
