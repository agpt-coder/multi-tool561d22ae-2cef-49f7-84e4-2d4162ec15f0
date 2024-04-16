---
date: 2024-04-16T09:06:34.171875
author: AutoGPT <info@agpt.co>
---

# multi tool

The Multi-Purpose API Toolkit is designed to offer a wide range of functionality through a single endpoint, making it easier for developers to integrate its features without the need for multiple third-party services. The toolkit provides a variety of endpoints including QR Code Generation, Currency Exchange Rate lookup, IP Geolocation services, Image Resizing, Password Strength Checking, Text-to-Speech conversion, Barcode Generation, Email Validation, Time Zone Conversion, URL Preview generation, PDF Watermarking, and converting RSS Feeds into JSON format. This comprehensive suite aims at simplifying and streamlining developers' tasks by providing a versatile set of tools for different needs, all accessible through one unified API.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'multi tool'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
