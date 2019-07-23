import express from 'express'
import path from 'path'
import http from 'http'
import io from 'socket.io'

import { setupWebSockets } from './websockets'
import { getNetworkIPs } from './utils'

// Static server for the client app
const expressApp = express()
const server = http.createServer(expressApp)
const port = process.env.SEEDSHIP_PORT || 9000
// binds socket.io
const ioServer = io(server)

const clientRoot = path.join(__dirname, '../webclient')
const gameRoot = path.join(process.env.PWD || __dirname, 'game')

expressApp.use(express.static(clientRoot))

server.listen(port, () => {
    const goodIPs = getNetworkIPs()

    console.log('The players\' computer should connect in this address:')
    goodIPs.forEach(ip => {
        console.log(`http://${ip}:${port}\n`)
    })
    console.log('\nYou can mirror what they\'re typing by using this address:')
    goodIPs.forEach(ip => {
        console.log(`http://${ip}:${port}/host\n`)
    })
})

setupWebSockets(ioServer, gameRoot)