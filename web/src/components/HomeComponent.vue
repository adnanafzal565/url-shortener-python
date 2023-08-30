<template>
	<div class="container">
		<div class="row">
			<div class="offset-md-3 col-md-6">
				<form v-on:submit.prevent="shortenURL">
					<div class="form-group">
						<label class="form-label">Enter URL</label>
						<input type="url" autocomplete="off" name="url" placeholder="Enter URL" class="form-control" required />
					</div>

					<input type="submit" class="btn btn-primary" style="margin-top: 10px;" value="Shorten" />
				</form>

				<table class="table table-bordered" style="margin-top: 50px;">
					<thead>
						<tr>
							<th>URL</th>
							<th>Views</th>
							<th>Clicks</th>
							<th>Created at</th>
						</tr>
					</thead>

					<tbody>
						<tr v-for="(url, index) in urls">
							<td>
								<router-link v-bind:to="'/url/' + url.hash" v-text="url.hash"></router-link>
							</td>
							<td v-text="url.views"></td>
							<td v-text="url.clicks"></td>
							<td v-text="url.created_at"></td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>

<script>
	
	import axios from "axios"
	import swal from "sweetalert2"
	import { io } from "socket.io-client"
	import store from "../store"

	export default {
		name: "HomeComponent",

		computed: {
			user() {
				return store.getters.getUser
			}
		},

		data() {
			return {
				urls: [],
				socketIO: null
			}
		},

		methods: {
			async shortenURL() {
				const form = event.target
				const formData = new FormData(form)
				formData.append("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone)

				try {
					const response = await axios.post(
						this.$apiURL + "/shorten-url",
						formData,
						this.$headers
					)

					if (response.data.status == "success") {
						this.urls.unshift(response.data.url)
						form.reset()
					} else {
						swal.fire("Error", response.data.message, "error")
					}
				} catch (exp) {
					console.log(exp)
				}
			},

			async getData() {
				const formData = new FormData()
				formData.append("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone)

				try {
					const response = await axios.post(
						this.$apiURL + "/fetch-urls",
						formData,
						this.$headers
					)

					if (response.data.status == "success") {
						this.urls = response.data.urls
					}
				} catch (exp) {
					console.log(exp)
				}
			}
		},

		mounted() {
			this.getData()
		},

		watch: {
			user(to, from) {
				const self = this

				if (to != null && this.socketIO == null) {
					this.socketIO = io(this.$nodeURL)
					this.socketIO.emit("connected", to._id)

					this.socketIO.on("urlViewed", function (urlId) {
						for (let a = 0; a < self.urls.length; a++) {
							if (self.urls[a]._id == urlId) {
								self.urls[a].views++
							}
						}
					})

					this.socketIO.on("urlClicked", function (urlId) {
						for (let a = 0; a < self.urls.length; a++) {
							if (self.urls[a]._id == urlId) {
								self.urls[a].clicks++
							}
						}
					})
				}
			}
		}
	}
</script>