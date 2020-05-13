# microservices app

__Advertisement :)__

- This is my "Superior Grade" (don't know how it's called in your country) project it's not professional or nothing similar, it's just my try to learn new tech and introduce my self into micro services. This project was made with me during an intership
in a company so i didn't have much time to make this with all i wanted to do, so i will be updating it in my free time adding
better error handling and Oauth2 support.
- Feel free to use copy or send me feedback!

Hope you like the project!

## Project Structure

First of all the project is hosted in a Google Cloud Platform VM, running in ubuntu 18.04lts, and the 
PostgreSQL databases are running in a Google Cloud Platform Cloud SQL, the storage is hosted with Firebase Storage and
the NoSQL database is hosted with Firebase Realtime Database.

The github project is configured for localhost, the kong server will run by defualt in [localhost](http://localhost:8000),
all the other services will go in localhost.

| service | host | port |
|---------|------|------|
| kong | http://localhost | :8000 |
| konga | http://localhost | :1337 |
| auth | http://localhost | :3002 |
| profile | http://localhost | :8100 |
| chat | http://localhost | :5000 |
| posts | http://localhost | :3000 |
| notifications | http://localhost | :9000 |

##

> 📂**Server**
> > 📂**Kong**
> > > *I use Kong for handling the routing (Kong uses Nginx) and the auth, you can also handle logging, trafic etc. For easy configuration i use Konga UI*
> >
> > 📂**src**
> > > 📂**Auth**
> > > > *This API is programmed using compojure framework (Clojure) it basically call's to kong for creating the Basic Auth of the user and sends other petition to the profiles API for creating a profile for that user.*
> > >
> > > 📂**Profile**
> > > > *This API is programmed using fastapi framework (Python) it hosts al the data of profiles without email and password and store it in a postgresql database.*
> > >
> > > 📂**Chat**
> > > > *This API is programmed using .net CORE 3 (C#) and it hosts all the chat data and store it in a Firebase realtime database.*
> > >
> > > 📂**Posts**
> > > > *This API is programmed in Go and it hosts all the posts data and store it in a postgresql database.*
> > >
> > > 📂**Notifications**
> > > > *This API is programmed in Scala with SLICK and PLAY it get's the notifications and sends it to the specified device.*

![Image](./img/schema.png)

## Auth API setup

Create a constants.clj file in the auth core package

```clj
(ns auth.constants
  (:gen-class))

(def server-path (str "YOUR SERVER URL"))

(def api-key (str "YOUR SERVER API - KEY"))
```

Start DEV server

```bash
sudo lein run dev
```

Start PROD server

```bash
sudo lein run dev
```

## Profile API setup

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn main:app --reload --port 8100
```

## Chat API setup

Create Constants.cs file in the config folder

```cs
using System;

namespace AppChat.config
{
    public class ProjectConstants
    {
        public const string AuthSecret = "YOUT FIREBASE SECRET";
        public const string BasePath = "YOUR REALTIME DATABASE URL";
    }
}
```

Make migrations

```bash
dotnet ef migrations add {MigrationName}
```

Update database

```bash
dotnet ef database update
```

Run server

```bash
sudo dotnet run
```

## Posts

Get all dependencies

```bash
go get -d ./...
```

Run server DEV

```bash
sudo go run *.go
```

Run server PROD

```bash
sudo go build
```

## Notifications

Compile api

```bash
sbt compile
```

Run server

```bash
sbt run
```

![Alt text][id]

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"