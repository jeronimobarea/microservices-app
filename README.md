# microservices app

---
__Advertisement :)__

- This is my "Superior Grade" (don't know how it's called in your country) project it's not professional or nothing similar, it's just my try to learn new tech and introduce my self into micro services. This porject was made with me during an intership 
in a company so i didn't have much time to make this with all i wanted to do, so i will be updating it in my free time adding 
better error handling and Oauth2 support.
- Feel free to use copy or send me feedback!

Hope you like the project!

---

## Project Structure
---

First of all the project is hosted in a Google Cloud Platform VM, running in ubuntu 18.04lts, and the 
PostgreSQL databases are running in a Google Cloud Platform Cloud SQL, the storage is hosted with Firebase Storage and
the NoSQL database is hosted with Firebase Realtime Database.

> 📂**Server**
> > 📂**Kong**
> > > *I use Kong for handling the routing (Kong uses Nginx) and the auth, you can also handle logging, trafic etc.*
> >
> > 📂**src*
> > > > 📂**Auth**
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


## Auth API setup

Start server
```
   sudo lein run dev
```


![Alt text][id]

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"




