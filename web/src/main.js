import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from "vue-router"

import HomeComponent from "./components/HomeComponent.vue"
import URLComponent from "./components/URLComponent.vue"
import SignupComponent from "./components/SignupComponent.vue"
import LoginComponent from "./components/LoginComponent.vue"

const app = createApp(App)
app.config.globalProperties.$apiURL = "http://127.0.0.1:8000"
app.config.globalProperties.$nodeURL = "http://localhost:3000"
app.config.globalProperties.$accessTokenKey = "accessToken"
app.config.globalProperties.$headers = {
	headers: {
		"Authorization": "Bearer " + localStorage.getItem("accessToken")		
	}
}

const routes = [
	{ path: "/login", component: LoginComponent },
	{ path: "/signup", component: SignupComponent },
	{ path: "/url/:url", component: URLComponent },
	{ path: "/", component: HomeComponent }
]

const router = createRouter({
	history: createWebHistory(),
	routes
})

app.use(router)
app.mount('#app')
