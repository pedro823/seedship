import express from 'express'
import path from 'path'
import http from 'http'
import os from 'os'
import io from 'socket.io'
import * as nodepty from 'node-pty'

// flatMap implementation for finding IPs
const flatMap = <T, U>(array: T[], mapFunc: (x: T) => U[]) : U[] =>
    array.reduce((cumulus: U[], next: T) => [...mapFunc(next), ...cumulus], <U[]> []);

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
    // Figures out what IP the host is
    const interfaces = os.networkInterfaces()

    const goodIPs = flatMap(Object.values(interfaces), (interfaceList => 
        interfaceList.filter(iface => !iface.internal && iface.family === 'IPv4')
                     .map(iface => iface.address)
    ))

    console.log('The client will be able to connect in this address:')
    goodIPs.forEach(ip => {
        console.log(`http://${ip}:${port}`)
    })
})

// Socket connection handling
ioServer.on('connection', (socket: io.Socket) => {
    const seedship = nodepty.spawn('/usr/bin/python3', ['seedship'], {
        name: 'xterm-color',
        cwd: gameRoot,
    })

    seedship.on('data', (data) => {
        console.log(`output>>>${data}`)
        socket.emit('write', data)
    })

    socket.on('command', (data) => {
        console.log(`user>>>${data}`)
        seedship.write(data)
    })
    
    socket.on('disconnect', () => {
        seedship.kill()
    })
})