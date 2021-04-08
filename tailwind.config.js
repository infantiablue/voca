const colors = require("tailwindcss/colors");

module.exports = {
	purge: [],
	theme: {
		extend: {
			colors: {
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
