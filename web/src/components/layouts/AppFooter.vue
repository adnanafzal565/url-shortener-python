<template>
	<footer class="container-fluid" style="margin-top: 50px; background-color: #e9e9e9; padding: 25px;">
		<div class="row">
			<div class="col-md-6">
				<p style="margin-bottom: 0px; text-align: center;">
					&copy;&nbsp;<span v-text="year"></span>&nbsp;
					adnan-tech.com
				</p>
			</div>

			<div class="col-md-6">
				<p style="margin-bottom: 0px; text-align: left;">
					For customizations, contact us: <br /><br />
					<b>Email</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp;&nbsp;support@adnan-tech.com <br />
					<b>WhatsApp</b> &nbsp;&nbsp;&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp;+92 310 5461304
				</p>
			</div>
		</div>
	</footer>
</template>

<script>
	export default {
		name: "AppFooter",

		data() {
			return {
				year: new Date().getFullYear()
			}
		}
	}
</script>