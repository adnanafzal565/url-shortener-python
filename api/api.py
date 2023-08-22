import uvicorn, random, string, bcrypt, jwt, time, auth
from datetime import datetime, timezone as timezone_module, timedelta
from dateutil import tz
from fastapi import Request, Form
from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId
from config import jwt_secret, app, auth_app, db

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/logout")
def logout(access_token: Annotated[str, Form()]):
	try:
		payload = jwt.decode(access_token, jwt_secret, algorithms = "HS256")

		db["users"].find_one_and_update({
			"_id": ObjectId(payload["user_id"])
		}, {
			"$unset": {
				"access_token": 1
			}
		})

		return {
			"status": "success",
			"message": "User has been logged-out."
		}
	except Exception as error:
		return {
			"status": "error",
			"message": "You have been logged-out.",
			"error": str(error)
		}

@auth_app.post("/me")
def get_user(timezone: Annotated[str, Form()], access_token: Annotated[str, Form()], request: Request):

	user = request.state.user

	return {
		"status": "success",
		"message": "User has been fetched.",
		"user": {
			"_id": user["_id"],
			"name": user["name"],
			"email": user["email"]
		}
	}

@app.post("/login")
def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):

	user = db["users"].find_one({
		"email": email
	})

	if user == None:
		return {
			"status": "error",
			"message": "Email does not exists."
		}

	if bcrypt.checkpw(password.encode("UTF-8"), user["password"]) != True:
		return {
			"status": "error",
			"message": "Password is in-correct."
		}

	access_token = jwt.encode({
		"user_id": str(user["_id"]),
		"time": datetime.now(timezone_module.utc).timetuple(),
		"exp": datetime.now(timezone_module.utc) + timedelta(hours=24)
	}, jwt_secret, algorithm = "HS256")

	db["users"].find_one_and_update({
		"_id": user["_id"]
	}, {
		"$set": {
			"access_token": access_token
		}
	})

	return {
		"status": "success",
		"message": "Login successfully.",
		"access_token": access_token,
		"user": {
			"_id": str(user["_id"]),
			"name": user["name"],
			"email": user["email"]
		}
	}

@app.post("/signup")
def signup(name: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):

	user = db["users"].find_one({
		"email": email
	})

	if user != None:
		return {
			"status": "error",
			"message": "Email already exists."
		}

	db["users"].insert_one({
		"name": name,
		"email": email,
		"password": bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()),
		"created_at": datetime.now(timezone_module.utc)
	})

	return {
		"status": "success",
		"message": "Account has been created. Please login now."
	}

@app.post("/url-clicked")
def url_clicked(url: Annotated[str, Form()]):
	db["urls"].find_one_and_update({
		"hash": url
	}, {
		"$inc": {
			"clicks": 1
		}
	})

@app.post("/get-url")
def get_url(url: Annotated[str, Form()]):

	url = db["urls"].find_one({
		"hash": url
	})

	if (url == None):
		return {
			"status": "error",
			"message": "URL not found."
		}

	db["urls"].find_one_and_update({
		"_id": url["_id"]
	}, {
		"$inc": {
			"views": 1
		}
	})

	url["_id"] = str(url["_id"])

	return {
		"status": "success",
		"message": "Data has been fetched.",
		"url": url
	}

@auth_app.post("/fetch-urls")
def fetch_urls(timezone: Annotated[str, Form()], request: Request):
	user = request.state.user

	urls = db["urls"].find({
			"user._id": user["_id"]
		}).sort("created_at", -1)

	url_arr = []
	for url in urls:
		url["_id"] = str(url["_id"])
		url["views"] = url.get("views", 0)
		url["clicks"] = url.get("clicks", 0)
		url["created_at"] = convert_utc_to_local(timezone, url["created_at"])

		url_arr.append(url)

	return {
		"status": "success",
		"message": "Data has been fetched.",
		"urls": url_arr
	}

@auth_app.post("/shorten-url")
def shorten_url(url: Annotated[str, Form()], timezone: Annotated[str, Form()], request: Request):
	user = request.state.user

	while True:
		random_characters = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
		url_obj = db["urls"].find_one({
			"hash": random_characters
		})

		if (url_obj == None):
			break

	inserted_doc = {
		"_id": ObjectId(),
		"url": url,
		"hash": random_characters,
		"views": 0,
		"clicks": 0,
		"user": {
			"_id": user["_id"],
			"name": user["name"]
		},
		"created_at": datetime.now(timezone_module.utc)
	}

	db["urls"].insert_one(inserted_doc)
	inserted_doc["_id"] = str(inserted_doc["_id"])
	inserted_doc["created_at"] = convert_utc_to_local(timezone, inserted_doc["created_at"])

	return {
		"status": "success",
		"message": "URL has been shortened.",
		"url": inserted_doc
	}

def convert_utc_to_local(timezone, utc):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz(timezone)

	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	utc = utc.replace(tzinfo=from_zone)

	# Convert time zone
	utc = utc.astimezone(to_zone).strftime("%b %d, %Y %H:%M:%S")

	return utc

app.mount("/", auth_app)

if __name__ == "__main__":
	uvicorn.run(app, port=8000, host="127.0.0.1")
