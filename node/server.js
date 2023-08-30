const express = require("express")
const app = express()
const http = require("http").createServer(app)
const socketIO = require("socket.io")(http, {
	cors: {
		origin: "*"
	}
})

// database module
const mongodb = require("mongodb")

// // client used to connect with database
const MongoClient = mongodb.MongoClient

// // each Mongo document's unique ID
const ObjectId = mongodb.ObjectId

// Add headers before the routes are defined
app.use(function (req, res, next) {
    // Website you wish to allow to connect
    res.setHeader("Access-Control-Allow-Origin", "*")
 
    // Request methods you wish to allow
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, PATCH, DELETE")
 
    // Request headers you wish to allow
    res.setHeader("Access-Control-Allow-Headers", "X-Requested-With,content-type,Authorization")
 
    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader("Access-Control-Allow-Credentials", true)
 
    // Pass to next layer of middleware
    next()
})

const users = []
global.db = null

async function connectMongoDB() {
	if (global.db != null) {
		return
	}

	// connect with database
    const client = await MongoClient.connect("mongodb://localhost:27017", { useUnifiedTopology: true })
    global.db = client.db("url_shortener")

    console.log("Database connected...")
}

// const port = process.env.PORT || 3000
const port = 3000
http.listen(port, async function () {
	console.log("Server started...")
	
	socketIO.on("connection", function (socket) {

		socket.on("connected", function (userId) {
			users[userId] = socket.id
			console.log("Socket connected..." + socket.id)
		})

		socket.on("urlClicked", async function (_id) {
			await connectMongoDB()

			const url = await global.db.collection("urls").findOne({
				_id: ObjectId(_id)
			})

			if (url != null) {
				socketIO.to(users[url.user._id]).emit("urlClicked", url._id.toString())
			}
		})

		socket.on("urlViewed", async function (_id) {
			await connectMongoDB()

			const url = await global.db.collection("urls").findOne({
				_id: ObjectId(_id)
			})

			if (url != null) {
				socketIO.to(users[url.user._id]).emit("urlViewed", url._id.toString())
			}
		})
	})
})