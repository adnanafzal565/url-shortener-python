<template>
	<nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 50px; padding-left: 50px; padding-right: 50px;">
	  <div class="container-fluid">
	    <router-link class="navbar-brand" to="/">URL Shortener</router-link>
	    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
	      <span class="navbar-toggler-icon"></span>
	    </button>
	    <div class="collapse navbar-collapse" id="navbarSupportedContent">
	      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
	        <li class="nav-item">
	          <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
	        </li>

	        <template v-if="user == null">
		        <li class="nav-item">
		          <router-link class="nav-link" to="/login">Login</router-link>
		        </li>

		        <li class="nav-item">
		          <router-link class="nav-link" to="/signup">Sign up</router-link>
		        </li>
	        </template>

	        <li class="nav-item" v-else>
	          <a href="javascript:void(0)" v-on:click="logout" class="nav-link">Logout</a>
	        </li>

	      </ul>
	    </div>
	  </div>
	</nav>
</template>

<script>

	import "../../assets/css/bootstrap.css"
	import "../../assets/js/jquery.js"
	import "../../assets/js/bootstrap.js"

	import axios from "axios"
	import swal from "sweetalert2"
	import store from "../../store"

	export default {
		name: "AppHeader",

		computed: {
			user() {
				return store.getters.getUser
			}
		},

		methods: {
			async logout() {
				const formData = new FormData()
				formData.append("access_token", localStorage.getItem(this.$accessTokenKey))
				
				try {
                    const response = await axios.post(
                        this.$apiURL + "/logout",
                        formData
                    )
                    
                    if (response.data.status == "success") {
                    	store.commit("setUser", null)
                    	localStorage.removeItem(this.$accessTokenKey)
                    	this.$router.push("/login")
                    }
                } catch (exp) {
                    console.log(exp)
                }
			},

			async getData() {
				const formData = new FormData()
				formData.append("access_token", localStorage.getItem(this.$accessTokenKey))
				formData.append("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone)
				
				try {
                    const response = await axios.post(
                        this.$apiURL + "/me",
                        formData,
                        this.$headers
                    )
                    
                    if (response.data.status == "success") {
                    	store.commit("setUser", response.data.user)
                    }
                } catch (exp) {
                    console.log(exp)
                }
			}
		},

		mounted() {
			this.getData()
		}
	}
</script>