# README.md

0. Environment
    * Venv
    * Poetry

1. Collecting data
    * Setting up GMail
    * Setting up S3 (optional)
    * AWS Lambda code

2. Visualizing / exploring data
    * Any senders that show up multiple times?
    * Any known phishing links?
      * use [Google Safe Browsing API](https://developers.google.com/safe-browsing/v4/lookup-api)

3. Models - spam vs. not spam
    * a) Bag-of-words + Multinomial Naive Bayes
    * b) LSTM

4. ...

## 0. Environment

### Venv

  ```python
  python -m venv ./venv
  ```

### Poetry

  ```bash
  poetry export -f requirements.txt --outputrequirements.txt
  ```

## Collecting data

1. Generate an application password for your gmail account. I called mine "AWS Lambda", but you can call it whatever you want. To do this, go to your GMail account (click on profile picture) > "Manage your google account" > Security tab > Signing in to Google > App Passwords, then create a password for Mail.

2. Set up IMAP. In Gmail itself, click on the gear icon to open Settings. Then go to the "Forwarding and POP/IMAP" tab. Scroll down to IMAP Access and make sure IMAP is enabled.

3. Create dynamodb table (use provided script)

4. Set up Lambda layer - [reference](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-update-venv). Running `generate_lambda_deployment_package.sh` does all this for you. Then add the layer to the lambda (in console -> scroll down below the Cloud9 editor to Layers and attach the layer)

  * make sure to increase timeout to ~15 mins

  <!-- * make sure to -->

## Data exploration

* Note : 677 emails are labeled as 'spam' out of X emails total ("Messages that have been in Spam more than 30 days will be automatically deleted.
") - therefore, for this exercise I'll also try to frame as an anomaly detection problem. In practice, over X% of email is spam (SOURCE?).

* For a quick comparison - in the last 30 days, I have 677 spam emails but X 'real' inbox emails, and of the real inbox emails, Y are from mailing lists / coupon lists / stores

## Models

### Multinomial N.B - spam vs. nonspam

### LSTM - spam vs. nonspam

### Other

TODO - decide various ways to explore data (classifying spam category? ex. phishing vs social engineering)

---

## Project Details

### Tests

`python -m gmail_spam.tests.{testfilename}`

### Documentation

Trying to stick to [numpydoc](https://numpydoc.readthedocs.io/en/v1.2.1/example.html#example) format