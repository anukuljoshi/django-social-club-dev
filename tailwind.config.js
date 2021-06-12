module.exports = {
  purge: {
    enabled: true,
    content: [
      './templates/**/*.html',
      './posts/templates/**/*.html',
      './users/templates/**/*.html',
      './static/js/**/*.js'
    ]
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        'koho': ['KoHo', 'Helvetica','sans-serif'],
        'noto': ['Noto Sans JP', 'sans-serif']
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
