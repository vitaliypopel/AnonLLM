
const csrf = document.cookie.split('; ')
                            .find(row => row.startsWith('csrftoken='))
                            ?.split('=')[1]

axios.defaults.headers.common['X-CSRFToken'] = csrf

const ask() => {
  axios.post('/api/ask/', {
      question: 'Hello! Who are you?'
    })
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })
}
