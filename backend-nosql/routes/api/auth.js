var express = require('express');
var router = express.Router();
var UserModel = require('../../models/user')

router.post('/signin', async (req, res, next) => {
    console.log(req.session);
    try {
        const {username, password} = req.body;
        console.log(typeof username, typeof password)

        console.log(username, password);

        if (username == 'chungdinh' && password == '123') {
            req.session.user = {
                name: 'chungdinh'
            }
            await req.session.save();

            console.log(req.session)
            return res.redirect('/dashboard');
        } else {
            res.status(401).json({ message: 'Invalid credential!'})
            return ;
        }
        
    } catch (err) {
        console.log(err);
        res.status(500).json({ message: 'Internal server error' });
    }
})

router.post('/signup', async (req, res, next) => {
    try {
        const {username, email, password} = req.body;

        if (!username || !email || !password) {
            res.status(400).json({message: 'Username, email and password are required!'});
            return ;
        }

        const existUser = await UserModel.findOne({
            username
        });

        if (existUser) {
            res.status(401).json({message: 'Email already used!'})
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = new UserModel({
            username,
            email,
            password: hashedPassword
        })

        await newUser.save();
        res.redirect('/signin')
    } catch (err) {
        console.log(err);
        res.status(500).json({ message: 'Internal server error' });
    }
});

router.get('/logout', (req, res, next) => {
    try {
        req.session.destroy();
        res.redirect('/');
    } catch (err) {
        console.log(err);
        res.status(500).json({ message: 'Internal server error' });
    }
})

module.exports = router