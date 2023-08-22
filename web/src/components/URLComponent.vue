<template>
	<div class="container">
		<div class="row">
			<div class="col-md-12">
				<div class="float-end" style="padding: 15px;
				    border-radius: 5px;
				    background-color: lightblue;
				    cursor: pointer;">
				    <span v-if="remaining_seconds > 0">
				    	Redirecting in <span v-text="remaining_seconds"></span> seconds
				    </span>
					
				    <span v-else v-on:click="goto_website">Go to website</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

	import axios from "axios"
	import swal from "sweetalert2"
	import detectChangeUrl from "detect-url-change"

	export default {
		name: "URLComponent",

		data() {
			return {
				url: this.$route.params.url,
				remaining_seconds: 5,
				url_obj: null,
				interval: null
			}
		},

		methods: {
			async goto_website() {
				if (this.url_obj == null) {
					return
				}

				const formData = new FormData()
				formData.append("url", this.url)
				window.navigator.sendBeacon((this.$api_url + "/url-clicked"), formData)

				window.location.href = this.url_obj.url
			},

			async getData() {
				const formData = new FormData()
				formData.append("url", this.url)

				try {
					const response = await axios.post(
						this.$api_url + "/get-url",
						formData
					)

					if (response.data.status == "success") {
						this.url_obj = response.data.url
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
					self.remaining_seconds--

					if (self.remaining_seconds <= 0) {
						clearInterval(self.interval)

						if (self.url_obj != null) {
							// window.location.href = self.url_obj.url
						}
					}
				}, 1000)
			}, 500)
		}
	}
</script>