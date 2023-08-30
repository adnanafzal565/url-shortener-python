<template>
	<div class="container">
		<div class="row">
			<div class="col-md-12">
				<div class="float-end" style="padding: 15px;
				    border-radius: 5px;
				    background-color: lightblue;
				    cursor: pointer;">
				    <span v-if="remainingSeconds > 0">
				    	Redirecting in <span v-text="remainingSeconds"></span> seconds
				    </span>
					
				    <span v-else v-on:click="gotoWebsite">Go to website</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

	import axios from "axios"
	import swal from "sweetalert2"
	import detectChangeUrl from "detect-url-change"
	import { io } from "socket.io-client"

	export default {
		name: "URLComponent",

		data() {
			return {
				url: this.$route.params.url,
				remainingSeconds: 5,
				urlObj: null,
				interval: null,
				socketIO: null
			}
		},

		methods: {
			async gotoWebsite() {
				if (this.urlObj == null) {
					return
				}

				if (this.socketIO != null) {
					this.socketIO.emit("urlClicked", this.urlObj._id)
				}

				const formData = new FormData()
				formData.append("url", this.url)
				window.navigator.sendBeacon((this.$apiURL + "/url-clicked"), formData)

				window.location.href = this.urlObj.url
			},

			async getData() {
				const formData = new FormData()
				formData.append("url", this.url)

				try {
					const response = await axios.post(
						this.$apiURL + "/get-url",
						formData
					)

					if (response.data.status == "success") {
						this.urlObj = response.data.url

						this.socketIO = io(this.$nodeURL)
						this.socketIO.emit("urlViewed", this.urlObj._id)
					} else {
						swal.fire("Error", response.data.message, "error")
					}
				} catch (exp) {
					console.log(exp)
				}
			}
		},

		mounted() {
			const self = this
			this.getData()

			detectChangeUrl.on('change', function (newUrl) {
				clearInterval(self.interval)
			})

			setTimeout(function () {
				self.interval = setInterval(function () {
					self.remainingSeconds--

					if (self.remainingSeconds <= 0) {
						clearInterval(self.interval)

						if (self.urlObj != null) {
							// window.location.href = self.urlObj.url
						}
					}
				}, 1000)
			}, 500)
		}
	}
</script>