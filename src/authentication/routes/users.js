var express = require('express');
var http = require('http');
var request = require('request');

var router = express.Router();

/* GET users listing. */
var userData = {}

var createConsumer = async function (req) {
    const consumerOptions = {
        host: '34.76.34.119',
        port: 8000,
        path: '/api/v1/auth/consumers/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api_key': 'ij8Z2ho2Dxl60kh3bcp1pfkxidhF8p3k'
        },
    }
    var kongConsumer = await http.request(consumerOptions, res => {
        console.log(`createConsumer -> statusCode: ${res.statusCode}`)

        res.on('data', (d) => {
            createAuth(req);
        })
        res.on('error', (error) => {
            console.error(error)
        })
    });

    await kongConsumer.write(JSON.stringify({
        'username': req.body['email']
    }));
    await kongConsumer.end();
}

var createAuth = async function (req) {
    const authOptions = {
        host: '34.76.34.119',
        port: 8000,
        path: '/api/v1/auth/consumers/' + req.body['email'].toString() + '/basic-auth',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api_key': 'ij8Z2ho2Dxl60kh3bcp1pfkxidhF8p3k'
        },
    }
    var kongAuth = await http.request(authOptions, res => {
        console.log(`kongAuth -> statusCode: ${res.statusCode}`)

        res.on('data', (d) => {
        })
        res.on('error', (error) => {
            console.error(error)
        })
    });

    await kongAuth.write(JSON.stringify({
        'username': req.body['email'],
        'password': req.body['password']
    }));
    await kongAuth.end();
}

var createProfile = async function (req) {
    const profileOptions = {
        host: '34.76.34.119',
        port: 8000,
        path: '/api/v1/pr/profiles/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api_key': 'ij8Z2ho2Dxl60kh3bcp1pfkxidhF8p3k'
        },
    }

    var createProfile = await http.request(profileOptions, (res) => {
        console.log(`createProfile -> statusCode: ${res.statusCode}`)

        res.on('data', function (chunk) {
            let id = chunk.toString()
            addCustomId(req, JSON.parse(id)['id']);
            userData.id = JSON.parse(id)['id'];
        });

        res.on('error', (error) => {
            console.error(error);
        });
    });

    await createProfile.write(JSON.stringify({
        'email': req.body['email']
    }));
    createProfile.end();
}

var addCustomId = async function (req, id) {
    const updateOptions = {
        host: '34.76.34.119',
        port: 8000,
        path: '/api/v1/auth/consumers/' + req.body['email'],
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'api_key': 'ij8Z2ho2Dxl60kh3bcp1pfkxidhF8p3k'
        },
    }

    var updateConsumer = await http.request(updateOptions, res => {
        console.log(`updateId -> statusCode: ${res.statusCode}`)

        res.on('data', (d) => {
        })
        res.on('error', (error) => {
            console.error(error)
        })
    });

    await updateConsumer.write(JSON.stringify({
        'custom_id': id
    }));
    await updateConsumer.end();
}

router.post('/register', async function (req, res, next) {

    try {
        await createConsumer(req);
        await createProfile(req);
    } catch (e) {
        throw e
    }
    userData.email = req.body['email']
    console.log(userData)
    res.send(userData);
});

router.get('/login', async function (req, res, next) {

    const profileOptions = {
        uri: 'http://34.76.34.119:8000/api/v1/auth/basic-auths/' + req.body['email'],
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'api_key': 'ij8Z2ho2Dxl60kh3bcp1pfkxidhF8p3k'
        },
    }


    request.get(profileOptions, (err, res, body) => {
        if (err) {
            return console.log(err);
        }
        console.log(JSON.parse(body));
        data = JSON.parse(body)

        checkPassword(req.body['password'], data['password'])
    });
    res.send(data);
});

module.exports = router;
