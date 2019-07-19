import express from 'express'
import path from 'path'
import http from 'http'
import io from 'socket.io'

const expressApp = express()
const server = http.createServer(expressApp)
const port = process.env.SEEDSHIP_PORT || 9000
const clientRoot = path.join(__dirname, '../webclient')
console.log(clientRoot)
const ioServer = io(server)

expressApp.use(express.static(clientRoot))

server.listen(port, () => {
    console.log(`listening at port ${port}`)
})

ioServer.on('connection', (socket: io.Socket) => {
    console.log('an user connected')

    socket.on('disconnect', () => {
        console.log('an user disconnected')
    })
})