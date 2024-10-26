/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      flex: {
        '4': '4 4 0%',
        '1': '1 1 0%',
      },
    },
  },
  plugins: [],
}

