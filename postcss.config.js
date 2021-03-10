const path = require("path");

module.exports = (ctx) => ({
	plugins: [
		require("tailwindcss")(path.resolve(__dirname, "tailwind.config.js")),
		require("autoprefixer"),
		ctx.env === "production" &&
			require("@fullhuman/postcss-purgecss")({
				content: [path.resolve(__dirname, "app/templates/**/*.html")],
				css: [path.resolve(__dirname, "app/static/src/css/*.css")],
				rejected: true,
				defaultExtractor: (content) => content.match(/[A-Za-z0-9-_:/]+/g) || [],
				safelist: [/^nav-/, /^alert-/, "alert"],
			}),
	],
});
