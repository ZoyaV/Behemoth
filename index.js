const express = require('express')
const app = express()
const port = 3000

app.use(express.static(__dirname + '/js'));
app.use(express.static(__dirname + '/css'));
app.use(express.static(__dirname + '/vendor'));
app.use(express.static(__dirname + '/img'));
app.use(express.static(__dirname + '/node_modules'));

app.get('/', (req, res) => {
  res.sendFile('index.html', {
    root: './'
  })
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})