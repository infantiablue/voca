const colors = require("tailwindcss/colors");

module.exports = {
	purge: [],
	theme: {
		extend: {
			colors: {
				// primary: "#1d3557",
				// secondary: "#2a9d8f",
				// highlight: "#f4a261",
				gray: colors.coolGray,
				blue: colors.lightBlue,
				green: colors.emerald,
				red: colors.rose,
			},
			fontFamily: {
				sans: ["Graphik", "sans-serif"],
				serif: ["Merriweather", "serif"],
			},
		},
	},
	variants: {},
	plugins: [require("@tailwindcss/forms")],
};
