const csrf = document.cookie.split('; ')
                            .find(row => row.startsWith('csrftoken='))
                            ?.split('=')[1]

axios.defaults.headers.common['X-CSRFToken'] = csrf
axios.defaults.headers.common['Content-Type'] = 'application/json'

const chatContainer = document.getElementsByClassName('chat')[0]

window.onload = () => {
  chatContainer.scrollTop = chatContainer.scrollHeight
}

const autoGrow = (element) => {
  element.style.height = "20vh"
}

const removeQuickStart = () => {
  var quickStartContainer = document.getElementsByClassName('quick-start')[0]
  if (quickStartContainer) {
    quickStartContainer.remove()
  }
}

const messageBtnEvent = () => {
  var message = document.getElementById('message')
  ask(message.value)
}

const messageBtn = document.getElementById('message-btn')
messageBtn.addEventListener('click', messageBtnEvent)

const createAnswer = (answer) => {
  var llmMessage = document.createElement('div')
  llmMessage.className = 'llm-message m-1 float-start message-width'

  var messageCard = document.createElement('div')
  messageCard.className = 'card llm-message-card'

  var messageCardBody = document.createElement('div')
  messageCardBody.className = 'card-body'

  var messageCardText = document.createElement('p')
  messageCardText.className = 'card-text'
  messageCardText.innerText = answer

  messageCardBody.appendChild(messageCardText)
  messageCard.appendChild(messageCardBody)
  llmMessage.appendChild(messageCard)

  chatContainer.appendChild(llmMessage)

  chatContainer.scrollTop = chatContainer.scrollHeight
}

const createQuestion = (question) => {
  var userMessage = document.createElement('div')
  userMessage.className = 'user-message m-1 float-end message-width'

  var messageCard = document.createElement('div')
  messageCard.className = 'card user-message-card'

  var messageCardBody = document.createElement('div')
  messageCardBody.className = 'card-body'

  var messageCardText = document.createElement('p')
  messageCardText.className = 'card-text'
  messageCardText.innerText = question

  messageCardBody.appendChild(messageCardText)
  messageCard.appendChild(messageCardBody)
  userMessage.appendChild(messageCard)

  chatContainer.appendChild(userMessage)

  createAnswer('Please wait a few seconds...')

  chatContainer.scrollTop = chatContainer.scrollHeight
}

const ask = (question) => {
  var message = document.getElementById('message')
  message.value = ''
  message.style.height = '30px'

  messageBtn.removeEventListener('click', messageBtnEvent)

  removeQuickStart()
  createQuestion(question)

  axios.post('/api/ask/', {
      question: question
    })
    .then((response) => {
      chatContainer.lastChild.remove()
      if (response.data.error) {
        alert(response.data.error)
        chatContainer.lastChild.remove()
      } else {
        createAnswer(response.data.answer)
      }
      messageBtn.addEventListener('click', messageBtnEvent)
    })
    .catch((error) => {
      console.log(error)
    })
}

const helloBtn = document.getElementById('q-hello')
const langsBtn = document.getElementById('q-lang')
const treeBtn = document.getElementById('q-tree')

if (helloBtn && langsBtn && treeBtn) {
  helloBtn.addEventListener('click', () => ask(helloBtn.innerText))
  langsBtn.addEventListener('click', () => ask(langsBtn.innerText))
  treeBtn.addEventListener('click', () => ask(treeBtn.innerText))
}
